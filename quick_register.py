import requests

def quick_register():
    # You can change these to whatever you want
    username = "your_username_here"  # Change this!
    password = "your_password_here"   # Change this!
    
    print(f"Registering user: {username}")
    
    url = "http://localhost:5001/api/register"
    data = {"username": username, "password": password}
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("✅ Registration successful!")
            print(f"Username: {username}")
            print("You can now login at http://localhost:3000")
        else:
            print(f"❌ Registration failed: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    quick_register()
