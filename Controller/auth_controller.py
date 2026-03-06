# Controller/auth_controller.py
from Model.user_model import UserModel
import re

class AuthController:
    """Handles authentication logic and validation"""

    @staticmethod
    def validate_email(email):
        """Validate email format using regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_signup(username, email, password, confirm_password):
        """Validate signup form inputs"""

        # Check if all fields are filled
        if not username or not email or not password or not confirm_password:
            return False, "All fields are required"

        # Check username length
        if len(username) < 3:
            return False, "Username must be at least 3 characters"

        # Check if username contains only valid characters
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"

        # Validate email format
        if not AuthController.validate_email(email):
            return False, "Invalid email format"

        # Check password length
        if len(password) < 6:
            return False, "Password must be at least 6 characters"

        # Check if passwords match
        if password != confirm_password:
            return False, "Passwords do not match"

        return True, "Validation passed"

    @staticmethod
    def register(username, email, password, confirm_password):
        """Handle user registration"""

        # Validate inputs first
        is_valid, message = AuthController.validate_signup(
            username, email, password, confirm_password
        )
        if not is_valid:
            return False, message

        # If validation passes, register in database
        success, message = UserModel.register_user(username, email, password)
        return success, message

    @staticmethod
    def login(username_or_email, password):
        """Handle user login"""

        # Check if fields are not empty
        if not username_or_email or not password:
            return False, "Please enter username/email and password", None

        # Attempt login through model
        success, message, user_data = UserModel.login_user(username_or_email, password)
        return success, message, user_data

    @staticmethod
    def admin_login(username, password):
        """Handle admin login"""

        # Check if fields are not empty
        if not username or not password:
            return False, "Please enter admin credentials", None

        # Attempt admin login through model
        success, message, admin_data = UserModel.login_admin(username, password)
        return success, message, admin_data

    @staticmethod
    def reset_password(email, new_password, confirm_password):
        """Handle password reset"""

        # Validate email
        if not email:
            return False, "Please enter your email"

        if not AuthController.validate_email(email):
            return False, "Invalid email format"

        # Validate new password
        if not new_password or not confirm_password:
            return False, "Please enter new password and confirmation"

        if len(new_password) < 6:
            return False, "Password must be at least 6 characters"

        if new_password != confirm_password:
            return False, "Passwords do not match"

        # Attempt password reset through model
        success, message = UserModel.reset_password(email, new_password)
        return success, message