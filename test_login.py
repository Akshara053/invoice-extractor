import requests
import json

# Test the login API
def test_login():
    url = "http://localhost:5001/api/login"
    
    # Test with the new test user
    test_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    try:
        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if 'token' in data:
                print("✅ Login successful!")
                print(f"Token: {data['token'][:50]}...")
                return data['token']
            else:
                print("❌ No token in response")
        else:
            print("❌ Login failed")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the Flask app is running on port 5001")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing login API...")
    test_login()
