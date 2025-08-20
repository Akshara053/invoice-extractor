import requests
import json

def register_user():
    print("=== User Registration ===")
    
    # Get user input
    username = input("Enter your desired username: ")
    password = input("Enter your desired password: ")
    
    # Register the user
    url = "http://localhost:5001/api/register"
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
            print(f"Username: {username}")
            print("You can now login with these credentials!")
        else:
            print("❌ Registration failed")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the Flask app is running on port 5001")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    register_user()
