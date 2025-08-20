import sqlite3
import hashlib

def create_test_user():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Create a test user
    test_username = "testuser"
    test_password = "password123"
    
    # Hash the password
    hashed_password = hashlib.sha256(test_password.encode()).hexdigest()
    
    try:
        # Check if user already exists
        cursor.execute("SELECT username FROM users WHERE username = ?", (test_username,))
        if cursor.fetchone():
            print(f"User '{test_username}' already exists")
        else:
            # Insert new user
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (test_username, hashed_password)
            )
            conn.commit()
            print(f"✅ Created test user: {test_username}")
            print(f"Password: {test_password}")
            print("You can now use these credentials to login!")
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_test_user()
