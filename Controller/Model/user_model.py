# Model/user_model.py
import hashlib
from Model.database import Database


class UserModel:
    """Handles all user-related database operations"""

    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register_user(username, email, password):
        """Register new user in database"""
        print(f"🔹 register_user called with: {username}, {email}")

        connection = Database.get_connection()
        if not connection:
            print("❌ Database connection is None")
            return False, "Database connection failed"

        print("✅ Database connection obtained")

        try:
            cursor = connection.cursor()
            print("✅ Cursor created")

            # Check if username already exists
            print(f"🔍 Checking if username '{username}' exists...")
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                print(f"❌ Username '{username}' already exists")
                return False, "Username already exists"
            print("✅ Username is available")

            # Check if email already exists
            print(f"🔍 Checking if email '{email}' exists...")
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_email = cursor.fetchone()
            if existing_email:
                print(f"❌ Email '{email}' already registered")
                return False, "Email already registered"
            print("✅ Email is available")

            # Hash password
            hashed_password = UserModel.hash_password(password)
            print(f"✅ Password hashed: {hashed_password[:20]}...")

            # Insert new user
            query = """INSERT INTO users (username, email, password) 
                       VALUES (%s, %s, %s)"""
            print(f"📝 Executing INSERT query...")
            cursor.execute(query, (username, email, hashed_password))
            print(f"✅ Query executed, committing...")
            connection.commit()
            print(f"✅ Commit successful!")

            print(f"✅ User '{username}' registered successfully")
            return True, "Registration successful"

        except Exception as e:
            print(f"❌ Registration error: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error: {str(e)}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("🔒 Connection closed")

    @staticmethod
    def login_user(username_or_email, password):
        """Login user (customer)"""
        connection = Database.get_connection()
        if not connection:
            return False, "Database connection failed", None

        try:
            cursor = connection.cursor(dictionary=True)

            # Hash the input password
            hashed_password = UserModel.hash_password(password)

            # Check credentials (username or email)
            query = """SELECT * FROM users 
                       WHERE (username = %s OR email = %s) 
                       AND password = %s 
                       AND is_active = TRUE"""
            cursor.execute(query, (username_or_email, username_or_email, hashed_password))
            user = cursor.fetchone()

            if user:
                print(f"✅ User '{user['username']}' logged in")
                return True, "Login successful", user
            else:
                print("❌ Invalid credentials")
                return False, "Invalid username/email or password", None

        except Exception as e:
            print(f"❌ Login error: {e}")
            return False, f"Error: {str(e)}", None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def login_admin(username, password):
        """Login admin"""
        connection = Database.get_connection()
        if not connection:
            return False, "Database connection failed", None

        try:
            cursor = connection.cursor(dictionary=True)

            # Hash the input password
            hashed_password = UserModel.hash_password(password)

            # Check admin credentials
            query = """SELECT * FROM admins 
                       WHERE username = %s AND password = %s"""
            cursor.execute(query, (username, hashed_password))
            admin = cursor.fetchone()

            if admin:
                print(f"✅ Admin '{admin['username']}' logged in")
                return True, "Admin login successful", admin
            else:
                print("❌ Invalid admin credentials")
                return False, "Invalid admin credentials", None

        except Exception as e:
            print(f"❌ Admin login error: {e}")
            return False, f"Error: {str(e)}", None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def reset_password(email, new_password):
        """Reset user password by email"""
        from Model.database import Database
        connection = Database.get_connection()
        if not connection:
            return False, "Database connection failed"

        try:
            cursor = connection.cursor()

            # Check if email exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if not user:
                return False, "Email not found"

            # Hash new password and update
            hashed_password = UserModel.hash_password(new_password)
            query = "UPDATE users SET password = %s WHERE email = %s"
            cursor.execute(query, (hashed_password, email))
            connection.commit()

            print(f"✅ Password reset for email: {email}")
            return True, "Password reset successful"

        except Exception as e:
            print(f"❌ Password reset error: {e}")
            return False, f"Error: {str(e)}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()