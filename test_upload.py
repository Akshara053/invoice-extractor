import requests
import os

def test_upload():
    # First login to get a token
    login_url = "http://localhost:5001/api/login"
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    try:
        # Login
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.json()}")
            return
        
        token = login_response.json()['token']
        print(f"✅ Login successful! Token: {token[:50]}...")
        
        # Test upload with a sample PDF
        upload_url = "http://localhost:5001/api/upload"
        
        # Check if there's a sample PDF in the invoices folder
        sample_pdf = "invoices/your_invoice.pdf"
        if not os.path.exists(sample_pdf):
            print(f"❌ Sample PDF not found at {sample_pdf}")
            return
        
        # Prepare the upload
        with open(sample_pdf, 'rb') as f:
            files = {'file': ('test_invoice.pdf', f, 'application/pdf')}
            data = {'invoice_type': 'printed'}
            headers = {'Authorization': f'Bearer {token}'}
            
            print("📤 Uploading file...")
            upload_response = requests.post(upload_url, files=files, data=data, headers=headers)
            
            print(f"📊 Upload Status: {upload_response.status_code}")
            print(f"📊 Response: {upload_response.json()}")
            
            if upload_response.status_code == 200:
                print("✅ Upload successful!")
                data = upload_response.json()
                if data.get('excel_url'):
                    print(f"📊 Excel file: {data['excel_url']}")
                if data.get('word_url'):
                    print(f"📄 Word file: {data['word_url']}")
            else:
                print("❌ Upload failed")
                
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the Flask app is running on port 5001")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing file upload...")
    test_upload()
