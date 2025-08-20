from flask_cors import CORS
from flask import Flask, request, jsonify, send_from_directory
import os
import shutil
from werkzeug.utils import secure_filename
import subprocess
import hashlib
import jwt
import datetime
import sqlite3
import datetime as dt
import threading
import time

UPLOAD_FOLDER = 'uploads'
EXTRACTED_FOLDER = 'extracted_data'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
SECRET_KEY = 'supersecretkey'  # Change this in production

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global lock to prevent multiple OCR processes
ocr_lock = threading.Lock()

def get_db():
    conn = sqlite3.connect("users.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS uploads (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, original_filename TEXT, excel_filename TEXT, word_filename TEXT, invoice_type TEXT, upload_time TEXT)"
    )
    
    # Ensure all profile columns exist
    try:
        conn.execute("ALTER TABLE users ADD COLUMN email TEXT")
    except:
        pass
    try:
        conn.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
    except:
        pass
    try:
        conn.execute("ALTER TABLE users ADD COLUMN phone TEXT")
    except:
        pass
    try:
        conn.execute("ALTER TABLE users ADD COLUMN company TEXT")
    except:
        pass
    try:
        conn.execute("ALTER TABLE users ADD COLUMN address TEXT")
    except:
        pass
    try:
        conn.execute("ALTER TABLE users ADD COLUMN city TEXT")
    except:
        pass
    try:
        conn.execute("ALTER TABLE users ADD COLUMN state TEXT")
    except:
        pass
    try:
        conn.execute("ALTER TABLE users ADD COLUMN country TEXT")
    except:
        pass
    try:
        conn.execute("ALTER TABLE users ADD COLUMN zip TEXT")
    except:
        pass
    try:
        conn.execute("ALTER TABLE users ADD COLUMN bio TEXT")
    except:
        pass
    
    conn.commit()
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except Exception:
        return None

def init_uploads_table():
    conn = sqlite3.connect("users.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS uploads (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, original_filename TEXT, excel_filename TEXT, word_filename TEXT, invoice_type TEXT, upload_time TEXT)"
    )
    conn.close()

def cleanup_old_files():
    """Clean up old extracted files to prevent clutter"""
    try:
        files = os.listdir(EXTRACTED_FOLDER)
        current_time = time.time()
        
        for file in files:
            file_path = os.path.join(EXTRACTED_FOLDER, file)
            # Keep only files from last 24 hours
            if current_time - os.path.getctime(file_path) > 86400:  # 24 hours
                os.remove(file_path)
                print(f"Cleaned up old file: {file}")
    except Exception as e:
        print(f"Cleanup error: {e}")

def safe_run_ocr():
    """Safely run OCR with proper locking and error handling"""
    with ocr_lock:
        try:
            print("Starting OCR process...")
            # Clean up old files first
            cleanup_old_files()
            
            # Run the fixed OCR script
            result = subprocess.run(
                ['python', 'ocr_to_word_excel_fixed.py'], 
                check=True, 
                capture_output=True, 
                text=True,
                timeout=300  # 5 minute timeout
            )
            print("OCR completed successfully")
            return True, None
        except subprocess.TimeoutExpired:
            return False, "OCR process timed out"
        except subprocess.CalledProcessError as e:
            return False, f"OCR failed: {e.stderr}"
        except Exception as e:
            return False, f"OCR error: {str(e)}"

init_uploads_table()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cur.fetchone():
        conn.close()
        return jsonify({'error': 'Username already exists'}), 400
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User registered successfully'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row or row[0] != hash_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = generate_token(username)
    return jsonify({'token': token})

@app.route('/api/upload', methods=['POST'])
def upload_invoice():
    # Require authentication
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid token'}), 401
    token = auth_header.split(' ')[1]
    username = verify_token(token)
    if not username:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    # File upload logic
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Create unique filename to prevent conflicts
            timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = secure_filename(file.filename)
            base_name, ext = os.path.splitext(safe_filename)
            unique_filename = f"{base_name}_{timestamp}{ext}"
            
            # Save uploaded file
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(upload_path)
            
            # Prepare invoice processing
            invoices_dir = 'invoices'
            if not os.path.exists(invoices_dir):
                os.makedirs(invoices_dir)
            
            # Use unique filename for invoice processing
            invoice_path = os.path.join(invoices_dir, f'invoice_{timestamp}.pdf')
            shutil.copy(upload_path, invoice_path)
            
            # Update the OCR script to use the correct file
            update_ocr_script_path(invoice_path)
            
            # Run extraction script with proper locking
            invoice_type = request.form.get('invoice_type', 'printed')
            print(f"Processing invoice: {unique_filename} (type: {invoice_type})")
            
            success, error_msg = safe_run_ocr()
            if not success:
                return jsonify({'error': f'Extraction failed: {error_msg}'}), 500
            
            # Find the generated files
            files = os.listdir(EXTRACTED_FOLDER)
            excel_files = [f for f in files if f.endswith('.xlsx')]
            word_files = [f for f in files if f.endswith('.docx')]
            
            # Get the most recent files
            excel_file = max(excel_files, key=lambda x: os.path.getctime(os.path.join(EXTRACTED_FOLDER, x))) if excel_files else None
            word_file = max(word_files, key=lambda x: os.path.getctime(os.path.join(EXTRACTED_FOLDER, x))) if word_files else None
            
            # Save to database
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO uploads (username, original_filename, excel_filename, word_filename, invoice_type, upload_time) VALUES (?, ?, ?, ?, ?, ?)",
                (username, unique_filename, excel_file, word_file, invoice_type, dt.datetime.now().isoformat())
            )
            conn.commit()
            conn.close()
            
            # Clean up temporary files
            try:
                os.remove(upload_path)
                os.remove(invoice_path)
            except:
                pass
            
            return jsonify({
                'excel_url': f'/api/download/{excel_file}' if excel_file else None,
                'word_url': f'/api/download/{word_file}' if word_file else None,
                'message': 'Invoice processed successfully'
            })
            
        except Exception as e:
            print(f"Upload error: {e}")
            return jsonify({'error': f'Upload failed: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400

def update_ocr_script_path(new_path):
    """Update the OCR script to use the correct invoice path"""
    try:
        # Read the current OCR script
        with open('ocr_to_word_excel_fixed.py', 'r') as f:
            content = f.read()
        
        # Update the PDF path
        updated_content = content.replace(
            'PDF_PATH = "invoices/your_invoice.pdf"',
            f'PDF_PATH = "{new_path}"'
        )
        
        # Write back the updated script
        with open('ocr_to_word_excel_fixed.py', 'w') as f:
            f.write(updated_content)
            
    except Exception as e:
        print(f"Error updating OCR script: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/download/<filename>')
def download_file(filename):
    return send_from_directory(EXTRACTED_FOLDER, filename, as_attachment=True)

@app.route('/api/history', methods=['GET'])
def history():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid token'}), 401
    token = auth_header.split(' ')[1]
    username = verify_token(token)
    if not username:
        return jsonify({'error': 'Invalid or expired token'}), 401
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, original_filename, excel_filename, word_filename, invoice_type, upload_time FROM uploads WHERE username = ? ORDER BY upload_time DESC",
        (username,)
    )
    rows = cur.fetchall()
    conn.close()
    history = [
        {
            "id": row[0],
            "original_filename": row[1],
            "excel_filename": row[2],
            "word_filename": row[3],
            "invoice_type": row[4],
            "upload_time": row[5],
        }
        for row in rows
    ]
    return jsonify({"history": history})

@app.route('/api/profile', methods=['GET'])
def get_profile():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid token'}), 401
    token = auth_header.split(' ')[1]
    username = verify_token(token)
    if not username:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    conn = get_db()
    try:
        cur = conn.cursor()
        
        # First check if user exists
        cur.execute("SELECT username FROM users WHERE username = ?", (username,))
        user_exists = cur.fetchone()
        
        if not user_exists:
            conn.close()
            return jsonify({'error': 'User not found'}), 404
        
        # Get all profile data with safe defaults
        cur.execute("""
            SELECT 
                username,
                COALESCE(email, '') as email,
                COALESCE(full_name, '') as full_name,
                COALESCE(phone, '') as phone,
                COALESCE(company, '') as company,
                COALESCE(address, '') as address,
                COALESCE(city, '') as city,
                COALESCE(state, '') as state,
                COALESCE(country, '') as country,
                COALESCE(zip, '') as zip,
                COALESCE(bio, '') as bio
            FROM users 
            WHERE username = ?
        """, (username,))
        
        row = cur.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'error': 'Profile not found'}), 404
        
        return jsonify({
            'username': row[0],
            'email': row[1],
            'full_name': row[2],
            'phone': row[3],
            'company': row[4],
            'address': row[5],
            'city': row[6],
            'state': row[7],
            'country': row[8],
            'zip': row[9],
            'bio': row[10]
        })
        
    except Exception as e:
        conn.close()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/api/profile', methods=['POST'])
def update_profile():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid token'}), 401
    token = auth_header.split(' ')[1]
    username = verify_token(token)
    if not username:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email', '')
    full_name = data.get('full_name', '')
    phone = data.get('phone', '')
    company = data.get('company', '')
    address = data.get('address', '')
    city = data.get('city', '')
    state = data.get('state', '')
    country = data.get('country', '')
    zip_code = data.get('zip', '')
    bio = data.get('bio', '')
    
    conn = get_db()
    try:
        cur = conn.cursor()
        
        # Update the profile with all fields
        cur.execute(
            "UPDATE users SET email=?, full_name=?, phone=?, company=?, address=?, city=?, state=?, country=?, zip=?, bio=? WHERE username=?",
            (email, full_name, phone, company, address, city, state, country, zip_code, bio, username)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Profile updated successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting fixed API server...")
    print("Features:")
    print("- Thread-safe OCR processing")
    print("- Automatic file cleanup")
    print("- Better error handling")
    print("- Unique file naming")
    app.run(debug=True, port=5001)
