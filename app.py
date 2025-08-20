from flask import Flask, render_template_string, request, send_from_directory, redirect, url_for, flash
import os
import shutil
from werkzeug.utils import secure_filename
import subprocess

UPLOAD_FOLDER = 'uploads'
EXTRACTED_FOLDER = 'extracted_data'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

TEMPLATE = '''
<!doctype html>
<title>Invoice Extractor</title>
<h2>Invoice to Excel/Word Extractor</h2>
<p>Upload your invoice (PDF, PNG, JPG, JPEG). The system will extract data and provide Excel/Word downloads.</p>
<form method=post enctype=multipart/form-data>
  <input type=file name=file accept="application/pdf,image/png,image/jpeg,image/jpg">
  <input type=submit value=Upload>
</form>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul>
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
{% if excel_file and word_file %}
  <h3>Download Results:</h3>
  <a href="{{ url_for('download_file', filename=excel_file) }}">Download Excel</a><br>
  <a href="{{ url_for('download_file', filename=word_file) }}">Download Word</a>
{% endif %}
'''

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    excel_file = word_file = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            # Move uploaded file to invoices/your_invoice.<ext>
            invoices_dir = 'invoices'
            if not os.path.exists(invoices_dir):
                os.makedirs(invoices_dir)
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            dest_name = 'your_invoice' + (ext if ext in ['.pdf', '.png', '.jpg', '.jpeg'] else '.pdf')
            dest_path = os.path.join(invoices_dir, dest_name)
            shutil.copy(upload_path, dest_path)
            # Run extraction in-process using the fixed OCR pipeline
            try:
                from ocr_to_word_excel_fixed import process_invoice
                ok = process_invoice(dest_path)
                if not ok:
                    raise RuntimeError('OCR extraction failed')
            except Exception as e:
                flash(f'Error during extraction: {e}')
                return render_template_string(TEMPLATE, excel_file=None, word_file=None)
            # Find latest Excel and Word files
            files = os.listdir(EXTRACTED_FOLDER)
            excel_files = [f for f in files if f.endswith('.xlsx')]
            word_files = [f for f in files if f.endswith('.docx')]
            if excel_files:
                excel_file = max(excel_files, key=lambda x: os.path.getctime(os.path.join(EXTRACTED_FOLDER, x)))
            if word_files:
                word_file = max(word_files, key=lambda x: os.path.getctime(os.path.join(EXTRACTED_FOLDER, x)))
            flash('Extraction complete! Download your files below.')
        else:
            flash('Invalid file type. Please upload a PDF or image (PNG/JPG/JPEG).')
    return render_template_string(TEMPLATE, excel_file=excel_file, word_file=word_file)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(EXTRACTED_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 