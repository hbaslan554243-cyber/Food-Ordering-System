from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QMessageBox
from Controller.auth_controller import AuthController

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(563, 420)
        Dialog.setFixedSize(563, 420)  # Make window non-resizable
        Dialog.setStyleSheet("background-color: white;")

        # ============================================
        # LOGIN SCREEN (Image on LEFT, Form on RIGHT)
        # ============================================

        # Image Label (Left side) - Login image
        self.login_image = QtWidgets.QLabel(parent=Dialog)
        self.login_image.setGeometry(QtCore.QRect(0, 0, 281, 421))
        self.login_image.setText("")
        self.login_image.setPixmap(
            QtGui.QPixmap(r"C:\Users\keith baslan\Downloads\ChatGPT Image Jan 3, 2026, 12_45_44 PM.png"))
        self.login_image.setScaledContents(True)
        self.login_image.setObjectName("login_image")

        # LOGIN FORM WIDGET (Right side)
        self.login_widget = QtWidgets.QWidget(parent=Dialog)
        self.login_widget.setGeometry(QtCore.QRect(281, 0, 282, 420))
        self.login_widget.setStyleSheet("background-color: white;")

        # Welcome Back Title
        self.label_5 = QtWidgets.QLabel(parent=self.login_widget)
        self.label_5.setGeometry(QtCore.QRect(30, 10, 231, 41))
        self.label_5.setStyleSheet(
            "color: black; font-size: 25px; font-weight: bold; letter-spacing: 2px; background-color: transparent;")
        self.label_5.setText("WELCOME BACK!")

        # Subtitle
        self.label_6 = QtWidgets.QLabel(parent=self.login_widget)
        self.label_6.setGeometry(QtCore.QRect(30, 50, 221, 20))
        self.label_6.setStyleSheet("color: grey; font-size: 10px; font-weight: 600; background-color: transparent;")
        self.label_6.setText("Sign in with your Email/Username and Password")

        # Email/Username Input
        self.lineEdit = QtWidgets.QLineEdit(parent=self.login_widget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 90, 221, 31))
        self.lineEdit.setPlaceholderText("Email/Username")
        self.lineEdit.setStyleSheet(
            "QLineEdit { border: 2px solid #E0E0E0; border-radius: 8px; padding: 4px; font-size: 12px; } QLineEdit:focus { border: 2px solid red; }")

        # Password Input
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.login_widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(30, 140, 221, 31))
        self.lineEdit_2.setPlaceholderText("Password")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_2.setStyleSheet(
            "QLineEdit { border: 2px solid #E0E0E0; border-radius: 8px; padding: 4px; font-size: 12px; } QLineEdit:focus { border: 2px solid red; }")

        # Forgot Password
        self.label_7 = QtWidgets.QLabel(parent=self.login_widget)
        self.label_7.setGeometry(QtCore.QRect(170, 175, 121, 20))
        self.label_7.setStyleSheet(
            "QLabel { color: grey; font-size: 10px; font-weight: 600; background-color: transparent; text-decoration: underline; } QLabel:hover { color: red; }")
        self.label_7.setText("Forgot Password?")
        self.label_7.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        # Login Button
        self.pushButton = QtWidgets.QPushButton(parent=self.login_widget)
        self.pushButton.setGeometry(QtCore.QRect(30, 210, 221, 41))
        self.pushButton.setAutoDefault(False)
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #FF4444;
                box-shadow: 0 4px 8px rgba(255, 0, 0, 0.3);
            }
            QPushButton:pressed {
                background-color: #CC0000;
            }
        """)
        self.pushButton.setText("LOGIN")

        # Divider line and text
        self.label_2 = QtWidgets.QLabel(parent=self.login_widget)
        self.label_2.setGeometry(QtCore.QRect(30, 260, 71, 20))
        self.label_2.setText("_________________________")

        self.label_3 = QtWidgets.QLabel(parent=self.login_widget)
        self.label_3.setGeometry(QtCore.QRect(110, 270, 61, 16))
        self.label_3.setStyleSheet("color: black; font-size: 12px; font-weight: 600;")
        self.label_3.setText("or login as")

        self.label_4 = QtWidgets.QLabel(parent=self.login_widget)
        self.label_4.setGeometry(QtCore.QRect(180, 260, 71, 20))
        self.label_4.setText("_________________________")

        # Admin Button
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.login_widget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 300, 201, 31))
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: red;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
                border-color: #999999;
            }
            QPushButton:pressed {
                background-color: #E8E8E8;
            }
        """)
        self.pushButton_2.setText("Admin")

        # Don't have account label
        self.label_8 = QtWidgets.QLabel(parent=self.login_widget)
        self.label_8.setGeometry(QtCore.QRect(50, 370, 131, 20))
        self.label_8.setStyleSheet("color: grey; font-size: 10px; font-weight: 600; background-color: transparent;")
        self.label_8.setText("Don't Have an Account Yet?")

        # Sign Up link
        self.label_9 = QtWidgets.QLabel(parent=self.login_widget)
        self.label_9.setGeometry(QtCore.QRect(180, 370, 71, 21))
        self.label_9.setStyleSheet(
            "QLabel { color: black; font-size: 10px; font-weight: 600; background-color: transparent; text-decoration: underline; } QLabel:hover { color: red; }")
        self.label_9.setText("Sign Up here")
        self.label_9.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        # ============================================
        # SIGNUP SCREEN (Form on LEFT, Image on RIGHT)
        # ============================================

        # SIGNUP FORM WIDGET (Left side - starts off-screen left)
        self.signup_widget = QtWidgets.QWidget(parent=Dialog)
        self.signup_widget.setGeometry(QtCore.QRect(-282, 0, 282, 420))
        self.signup_widget.setStyleSheet("background-color: white;")

        # Create Account Title
        self.signup_title = QtWidgets.QLabel(parent=self.signup_widget)
        self.signup_title.setGeometry(QtCore.QRect(30, 10, 260, 41))
        self.signup_title.setStyleSheet(
            "color: black; font-size: 24px; font-weight: bold; letter-spacing: 1px; background-color: transparent;")
        self.signup_title.setText("Create an account")

        # Subtitle
        self.signup_subtitle = QtWidgets.QLabel(parent=self.signup_widget)
        self.signup_subtitle.setGeometry(QtCore.QRect(38, 50, 221, 20))
        self.signup_subtitle.setStyleSheet(
            "color: grey; font-size: 10px; font-weight: 600; background-color: transparent;")
        self.signup_subtitle.setText("Sign up with your valid email and password.")

        # Username Input
        self.signup_username = QtWidgets.QLineEdit(parent=self.signup_widget)
        self.signup_username.setGeometry(QtCore.QRect(30, 85, 221, 31))
        self.signup_username.setPlaceholderText("Username")
        self.signup_username.setStyleSheet(
            "QLineEdit { border: 2px solid #E0E0E0; border-radius: 15px; padding: 4px; font-size: 12px; } QLineEdit:focus { border: 2px solid red; }")

        # Email Input
        self.signup_email = QtWidgets.QLineEdit(parent=self.signup_widget)
        self.signup_email.setGeometry(QtCore.QRect(30, 130, 221, 31))
        self.signup_email.setPlaceholderText("Email")
        self.signup_email.setStyleSheet(
            "QLineEdit { border: 2px solid #E0E0E0; border-radius: 15px; padding: 4px; font-size: 12px; } QLineEdit:focus { border: 2px solid red; }")

        # Password Input
        self.signup_password = QtWidgets.QLineEdit(parent=self.signup_widget)
        self.signup_password.setGeometry(QtCore.QRect(30, 175, 221, 31))
        self.signup_password.setPlaceholderText("Password")
        self.signup_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.signup_password.setStyleSheet(
            "QLineEdit { border: 2px solid #E0E0E0; border-radius: 15px; padding: 4px; font-size: 12px; } QLineEdit:focus { border: 2px solid red; }")

        # Confirm Password Input
        self.signup_confirm = QtWidgets.QLineEdit(parent=self.signup_widget)
        self.signup_confirm.setGeometry(QtCore.QRect(30, 220, 221, 31))
        self.signup_confirm.setPlaceholderText("Confirm Password")
        self.signup_confirm.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.signup_confirm.setStyleSheet(
            "QLineEdit { border: 2px solid #E0E0E0; border-radius: 15px; padding: 4px; font-size: 12px; } QLineEdit:focus { border: 2px solid red; }")

        # Sign Up Button
        self.signup_button = QtWidgets.QPushButton(parent=self.signup_widget)
        self.signup_button.setGeometry(QtCore.QRect(30, 270, 221, 41))
        self.signup_button.setAutoDefault(False)
        self.signup_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #FF4444;
                box-shadow: 0 4px 8px rgba(255, 0, 0, 0.3);
            }
            QPushButton:pressed {
                background-color: #CC0000;
            }
        """)
        self.signup_button.setText("Sign Up")

        # Already have account label
        self.signup_login_text = QtWidgets.QLabel(parent=self.signup_widget)
        self.signup_login_text.setGeometry(QtCore.QRect(54, 360, 150, 20))
        self.signup_login_text.setStyleSheet(
            "color: grey; font-size: 10px; font-weight: 600; background-color: transparent;")
        self.signup_login_text.setText("Already Have an Account?")

        # Login link
        self.signup_login_link = QtWidgets.QLabel(parent=self.signup_widget)
        self.signup_login_link.setGeometry(QtCore.QRect(175, 360, 71, 21))
        self.signup_login_link.setStyleSheet(
            "QLabel { color: black; font-size: 10px; font-weight: 600; background-color: transparent; text-decoration: underline; } QLabel:hover { color: red; }")
        self.signup_login_link.setText("Login here")
        self.signup_login_link.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        # Signup Image (Right side - starts off-screen right)
        self.signup_image = QtWidgets.QLabel(parent=Dialog)
        self.signup_image.setGeometry(QtCore.QRect(563, 0, 281, 421))
        self.signup_image.setText("")
        self.signup_image.setPixmap(
            QtGui.QPixmap(r"C:\Users\keith baslan\Downloads\ChatGPT Image Jan 3, 2026, 05_54_25 PM.png"))
        self.signup_image.setScaledContents(True)
        self.signup_image.setObjectName("signup_image")

        # ============================================
        # ADMIN SCREEN (Centered frame with background)
        # ============================================

        # Admin background (full screen, starts off-screen bottom)
        self.admin_background = QtWidgets.QLabel(parent=Dialog)
        self.admin_background.setGeometry(QtCore.QRect(0, 420, 563, 420))
        self.admin_background.setText("")
        self.admin_background.setPixmap(QtGui.QPixmap(r"C:\Users\keith baslan\Downloads\ChatGPT Image Jan 4, 2026, 12_28_07 PM.png"))
        self.admin_background.setScaledContents(True)
        self.admin_background.setObjectName("admin_background")

        # Admin frame - centered with shadow
        self.admin_frame = QtWidgets.QFrame(parent=Dialog)
        self.admin_frame.setGeometry(QtCore.QRect(161, 470, 241, 320))
        self.admin_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 250);
                border: none;
                border-radius: 15px;
            }
        """)
        self.admin_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.admin_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.admin_frame.setObjectName("admin_frame")

        # Back button (top-left of frame)
        self.admin_back_button = QtWidgets.QPushButton(parent=self.admin_frame)
        self.admin_back_button.setGeometry(QtCore.QRect(10, 10, 30, 30))
        self.admin_back_button.setAutoDefault(False)
        self.admin_back_button.setText("←")
        self.admin_back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666;
                border: none;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        self.admin_back_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        # Admin logo
        self.admin_logo = QtWidgets.QLabel(parent=self.admin_frame)
        self.admin_logo.setGeometry(QtCore.QRect(70, 20, 101, 81))
        self.admin_logo.setText("")
        self.admin_logo.setPixmap(QtGui.QPixmap(r"C:\Users\keith baslan\Downloads\ChatGPT Image Jan 3, 2026, 07_20_26 PM.png"))
        self.admin_logo.setScaledContents(True)
        self.admin_logo.setObjectName("admin_logo")

        # Welcome Admin title
        self.admin_title = QtWidgets.QLabel(parent=self.admin_frame)
        self.admin_title.setGeometry(QtCore.QRect(40, 100, 161, 21))
        self.admin_title.setStyleSheet(
            "color: black; font-size: 15px; font-weight: bold; letter-spacing: 2px; background-color: transparent;")
        self.admin_title.setText("ADMIN LOGIN")
        self.admin_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Admin username input
        self.admin_username = QtWidgets.QLineEdit(parent=self.admin_frame)
        self.admin_username.setGeometry(QtCore.QRect(20, 140, 201, 35))
        self.admin_username.setPlaceholderText("Admin Username")
        self.admin_username.setStyleSheet("""
            QLineEdit {     
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 4px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid red;
            }
        """)

        # Admin password input
        self.admin_password = QtWidgets.QLineEdit(parent=self.admin_frame)
        self.admin_password.setGeometry(QtCore.QRect(20, 190, 201, 35))
        self.admin_password.setPlaceholderText("Admin Password")
        self.admin_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.admin_password.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 4px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid red;
            }
        """)

        # Admin login button
        self.admin_login_button = QtWidgets.QPushButton(parent=self.admin_frame)
        self.admin_login_button.setGeometry(QtCore.QRect(20, 245, 201, 40))
        self.admin_login_button.setAutoDefault(False)
        self.admin_login_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #FF4444;
                box-shadow: 0 4px 8px rgba(255, 0, 0, 0.3);
            }
            QPushButton:pressed {
                background-color: #CC0000;
            }
        """)
        self.admin_login_button.setText("LOGIN")

        # Connect click events
        self.label_9.mousePressEvent = lambda event: self.slide_to_signup(Dialog)
        self.signup_login_link.mousePressEvent = lambda event: self.slide_to_login(Dialog)
        self.pushButton_2.clicked.connect(lambda: self.slide_to_admin(Dialog))
        self.admin_back_button.clicked.connect(lambda: self.slide_from_admin_to_login(Dialog))

        # Connect authentication buttons
        self.signup_button.clicked.connect(self.handle_signup)
        self.pushButton.clicked.connect(self.handle_login)
        self.admin_login_button.clicked.connect(self.handle_admin_login)

        # Connect click events (existing code)
        self.label_9.mousePressEvent = lambda event: self.slide_to_signup(Dialog)
        self.signup_login_link.mousePressEvent = lambda event: self.slide_to_login(Dialog)
        self.pushButton_2.clicked.connect(lambda: self.slide_to_admin(Dialog))
        self.admin_back_button.clicked.connect(lambda: self.slide_from_admin_to_login(Dialog))

        # ============================================
        # FORGOT PASSWORD SCREEN (Centered dialog)
        # ============================================

        # Forgot password background (starts off-screen with image)
        self.forgot_bg = QtWidgets.QLabel(parent=Dialog)
        self.forgot_bg.setGeometry(QtCore.QRect(0, -420, 563, 420))
        self.forgot_bg.setText("")
        self.forgot_bg.setPixmap(
            QtGui.QPixmap(r"C:\Users\keith baslan\Downloads\ChatGPT Image Jan 4, 2026, 07_45_48 PM.png"))
        self.forgot_bg.setScaledContents(True)
        self.forgot_bg.setObjectName("forgot_bg")

        # Forgot password frame - centered
        # Forgot password frame - centered
        self.forgot_frame = QtWidgets.QFrame(parent=Dialog)
        self.forgot_frame.setGeometry(QtCore.QRect(131, -380, 301, 380))
        self.forgot_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: none;
                border-radius: 15px;
            }
        """)
        self.forgot_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.forgot_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.forgot_frame.setObjectName("forgot_frame")


        # Back button
        self.forgot_back_button = QtWidgets.QPushButton(parent=self.forgot_frame)
        self.forgot_back_button.setGeometry(QtCore.QRect(10, 10, 30, 30))
        self.forgot_back_button.setAutoDefault(False)
        self.forgot_back_button.setText("←")
        self.forgot_back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666;
                border: none;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        self.forgot_back_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        # Title
        self.forgot_title = QtWidgets.QLabel(parent=self.forgot_frame)
        self.forgot_title.setGeometry(QtCore.QRect(70, 50, 221, 31))
        self.forgot_title.setStyleSheet(
            "color: black; font-size: 20px; font-weight: bold; letter-spacing: 1px; background-color: transparent;")
        self.forgot_title.setText("Reset Password")

        # Subtitle
        self.forgot_subtitle = QtWidgets.QLabel(parent=self.forgot_frame)
        self.forgot_subtitle.setGeometry(QtCore.QRect(52, 85, 221, 40))
        self.forgot_subtitle.setStyleSheet(
            "color: grey; font-size: 12px; font-weight: 600; background-color: transparent;")
        self.forgot_subtitle.setText("Enter your email and new password")
        self.forgot_subtitle.setWordWrap(True)

        # Email input
        self.forgot_email = QtWidgets.QLineEdit(parent=self.forgot_frame)
        self.forgot_email.setGeometry(QtCore.QRect(40, 140, 221, 35))
        self.forgot_email.setPlaceholderText("Email")
        self.forgot_email.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 4px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid red;
            }
        """)

        # New password input
        self.forgot_new_password = QtWidgets.QLineEdit(parent=self.forgot_frame)
        self.forgot_new_password.setGeometry(QtCore.QRect(40, 190, 221, 35))
        self.forgot_new_password.setPlaceholderText("New Password")
        self.forgot_new_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.forgot_new_password.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 4px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid red;
            }
        """)

        # Confirm password input
        self.forgot_confirm_password = QtWidgets.QLineEdit(parent=self.forgot_frame)
        self.forgot_confirm_password.setGeometry(QtCore.QRect(40, 240, 221, 35))
        self.forgot_confirm_password.setPlaceholderText("Confirm New Password")
        self.forgot_confirm_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.forgot_confirm_password.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 4px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid red;
            }
        """)

        # Reset button
        self.forgot_reset_button = QtWidgets.QPushButton(parent=self.forgot_frame)
        self.forgot_reset_button.setGeometry(QtCore.QRect(40, 295, 221, 40))
        self.forgot_reset_button.setAutoDefault(False)
        self.forgot_reset_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #FF4444;
                box-shadow: 0 4px 8px rgba(255, 0, 0, 0.3);
            }
            QPushButton:pressed {
                background-color: #CC0000;
            }
        """)
        self.forgot_reset_button.setText("Reset Password")

        # Connect forgot password links
        self.label_7.mousePressEvent = lambda event: self.slide_to_forgot_password(Dialog)
        self.forgot_back_button.clicked.connect(lambda: self.slide_from_forgot_to_login(Dialog))
        self.forgot_reset_button.clicked.connect(self.handle_forgot_password)

        # Setup animations
        self.setup_animations(Dialog)
        self.Dialog = Dialog

    def setup_animations(self, Dialog):
        # Login widget animation
        self.login_widget_animation = QPropertyAnimation(self.login_widget, b"geometry")
        self.login_widget_animation.setDuration(600)
        self.login_widget_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Login image animation
        self.login_image_animation = QPropertyAnimation(self.login_image, b"geometry")
        self.login_image_animation.setDuration(600)
        self.login_image_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Signup widget animation
        self.signup_widget_animation = QPropertyAnimation(self.signup_widget, b"geometry")
        self.signup_widget_animation.setDuration(600)
        self.signup_widget_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Signup image animation
        self.signup_image_animation = QPropertyAnimation(self.signup_image, b"geometry")
        self.signup_image_animation.setDuration(600)
        self.signup_image_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Admin background animation
        self.admin_background_animation = QPropertyAnimation(self.admin_background, b"geometry")
        self.admin_background_animation.setDuration(600)
        self.admin_background_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Admin frame animation
        self.admin_frame_animation = QPropertyAnimation(self.admin_frame, b"geometry")
        self.admin_frame_animation.setDuration(600)
        self.admin_frame_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Forgot password background animation
        self.forgot_bg_animation = QPropertyAnimation(self.forgot_bg, b"geometry")
        self.forgot_bg_animation.setDuration(600)
        self.forgot_bg_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Forgot password frame animation
        self.forgot_frame_animation = QPropertyAnimation(self.forgot_frame, b"geometry")
        self.forgot_frame_animation.setDuration(600)
        self.forgot_frame_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def slide_to_signup(self, Dialog):
        """Transition: Login -> Signup"""
        # Login image slides out to the left
        self.login_image_animation.setStartValue(QtCore.QRect(0, 0, 281, 421))
        self.login_image_animation.setEndValue(QtCore.QRect(-281, 0, 281, 421))

        # Login form slides out to the right
        self.login_widget_animation.setStartValue(QtCore.QRect(281, 0, 282, 420))
        self.login_widget_animation.setEndValue(QtCore.QRect(563, 0, 282, 420))

        # Signup form slides in from left
        self.signup_widget_animation.setStartValue(QtCore.QRect(-282, 0, 282, 420))
        self.signup_widget_animation.setEndValue(QtCore.QRect(0, 0, 282, 420))

        # Signup image slides in from right
        self.signup_image_animation.setStartValue(QtCore.QRect(563, 0, 281, 421))
        self.signup_image_animation.setEndValue(QtCore.QRect(282, 0, 281, 421))

        # Start animations
        self.login_image_animation.start()
        self.login_widget_animation.start()
        self.signup_widget_animation.start()
        self.signup_image_animation.start()

    def slide_to_login(self, Dialog):
        """Transition: Signup -> Login"""
        # Signup form slides out to the left
        self.signup_widget_animation.setStartValue(QtCore.QRect(0, 0, 282, 420))
        self.signup_widget_animation.setEndValue(QtCore.QRect(-282, 0, 282, 420))

        # Signup image slides out to the right
        self.signup_image_animation.setStartValue(QtCore.QRect(282, 0, 281, 421))
        self.signup_image_animation.setEndValue(QtCore.QRect(563, 0, 281, 421))

        # Login image slides in from left
        self.login_image_animation.setStartValue(QtCore.QRect(-281, 0, 281, 421))
        self.login_image_animation.setEndValue(QtCore.QRect(0, 0, 281, 421))

        # Login form slides in from right
        self.login_widget_animation.setStartValue(QtCore.QRect(563, 0, 282, 420))
        self.login_widget_animation.setEndValue(QtCore.QRect(281, 0, 282, 420))

        # Start animations
        self.signup_widget_animation.start()
        self.signup_image_animation.start()
        self.login_image_animation.start()
        self.login_widget_animation.start()

    def slide_to_admin(self, Dialog):
        """Transition: Login -> Admin (image up, form down)"""
        # Login image slides UP (off-screen top)
        self.login_image_animation.setStartValue(QtCore.QRect(0, 0, 281, 421))
        self.login_image_animation.setEndValue(QtCore.QRect(0, -420, 281, 421))

        # Login form slides DOWN (off-screen bottom)
        self.login_widget_animation.setStartValue(QtCore.QRect(281, 0, 282, 420))
        self.login_widget_animation.setEndValue(QtCore.QRect(281, 420, 282, 420))

        # Admin background appears in center
        self.admin_background_animation.setStartValue(QtCore.QRect(0, 420, 563, 420))
        self.admin_background_animation.setEndValue(QtCore.QRect(0, 0, 563, 420))

        # Admin frame appears in center
        self.admin_frame_animation.setStartValue(QtCore.QRect(161, 480, 241, 320))
        self.admin_frame_animation.setEndValue(QtCore.QRect(161, 50, 241, 320))

        # Start animations
        self.login_image_animation.start()
        self.login_widget_animation.start()
        self.admin_background_animation.start()
        self.admin_frame_animation.start()

    def slide_from_admin_to_login(self, Dialog):
        """Transition: Admin -> Login (reverse of login to admin)"""
        # Admin background slides down
        self.admin_background_animation.setStartValue(QtCore.QRect(0, 0, 563, 420))
        self.admin_background_animation.setEndValue(QtCore.QRect(0, 420, 563, 420))

        # Admin frame slides down
        self.admin_frame_animation.setStartValue(QtCore.QRect(161, 50, 241, 320))
        self.admin_frame_animation.setEndValue(QtCore.QRect(161, 480, 241, 320))

        # Login image slides DOWN (from top)
        self.login_image_animation.setStartValue(QtCore.QRect(0, -420, 281, 421))
        self.login_image_animation.setEndValue(QtCore.QRect(0, 0, 281, 421))

        # Login form slides UP (from bottom)
        self.login_widget_animation.setStartValue(QtCore.QRect(281, 420, 282, 420))
        self.login_widget_animation.setEndValue(QtCore.QRect(281, 0, 282, 420))

        # Start animations
        self.admin_background_animation.start()
        self.admin_frame_animation.start()
        self.login_image_animation.start()
        self.login_widget_animation.start()

    def handle_signup(self):
        """Handle sign up button click"""
        try:
            username = self.signup_username.text().strip()
            email = self.signup_email.text().strip()
            password = self.signup_password.text()
            confirm = self.signup_confirm.text()

            print(f"📝 Attempting registration for: {username}, {email}")

            # Call controller
            success, message = AuthController.register(username, email, password, confirm)

            print(f"✅ Registration result: {success}, {message}")

            if success:
                QMessageBox.information(self.Dialog, "Success ✅",
                                        message + "\n\nYou can now login!")
                # Clear fields
                self.signup_username.clear()
                self.signup_email.clear()
                self.signup_password.clear()
                self.signup_confirm.clear()
                # Slide back to login
                self.slide_to_login(self.Dialog)
            else:
                QMessageBox.warning(self.Dialog, "Registration Failed ❌", message)

        except Exception as e:
            print(f"❌ ERROR in handle_signup: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.Dialog, "Error", f"An error occurred: {str(e)}")

    def handle_login(self):
        """Handle login button click"""
        username_or_email = self.lineEdit.text().strip()
        password = self.lineEdit_2.text()

        # Call controller
        success, message, user_data = AuthController.login(username_or_email, password)

        if success:
            print(f"🔹 User logged in: {user_data}")

            # Close login window
            self.Dialog.close()

            # Open Customer Dashboard
            self.open_customer_dashboard(user_data)
        else:
            QMessageBox.warning(None, "Login Failed ❌", message)

    def handle_admin_login(self):
        """Handle admin login button click"""
        username = self.admin_username.text().strip()
        password = self.admin_password.text()

        # Call controller
        success, message, admin_data = AuthController.admin_login(username, password)

        if success:
            print(f"🔹 Admin logged in: {admin_data}")

            # Close login window
            self.Dialog.close()

            # Open Admin Dashboard
            self.open_admin_dashboard()
        else:
            QMessageBox.warning(self.Dialog, "Login Failed ❌", message)

    def open_admin_dashboard(self):
        """Open Admin Dashboard window"""
        from View.AdminDashboard import Ui_Dialog as AdminUI

        self.admin_dialog = QtWidgets.QDialog()
        self.admin_ui = AdminUI()
        self.admin_ui.setupUi(self.admin_dialog)
        self.admin_dialog.show()

    def open_customer_dashboard(self, user_data):
        """Open Customer Dashboard window"""
        from View.CustomerDashboard import Ui_Dialog as CustomerUI

        self.customer_dialog = QtWidgets.QDialog()
        self.customer_ui = CustomerUI()
        self.customer_ui.set_user(user_data)  # Pass user data
        self.customer_ui.setupUi(self.customer_dialog)
        self.customer_dialog.show()

    def slide_to_forgot_password(self, Dialog):
        """Transition: Login -> Forgot Password (login splits apart, forgot slides from TOP)"""
        # Login image slides DOWN (off-screen bottom)
        self.login_image_animation.setStartValue(QtCore.QRect(0, 0, 281, 421))
        self.login_image_animation.setEndValue(QtCore.QRect(0, 420, 281, 421))

        # Login form slides UP (off-screen top) - opposite direction for split effect
        self.login_widget_animation.setStartValue(QtCore.QRect(281, 0, 282, 420))
        self.login_widget_animation.setEndValue(QtCore.QRect(281, -420, 282, 420))

        # Forgot password background slides DOWN from top
        self.forgot_bg_animation.setStartValue(QtCore.QRect(0, -420, 563, 420))
        self.forgot_bg_animation.setEndValue(QtCore.QRect(0, 0, 563, 420))

        # Forgot password frame slides DOWN from top
        self.forgot_frame_animation.setStartValue(QtCore.QRect(131, -380, 301, 380))
        self.forgot_frame_animation.setEndValue(QtCore.QRect(131, 20, 301, 380))

        # Start animations
        self.login_image_animation.start()
        self.login_widget_animation.start()
        self.forgot_bg_animation.start()
        self.forgot_frame_animation.start()

    def slide_from_forgot_to_login(self, Dialog):
        """Transition: Forgot Password -> Login (forgot slides to TOP, login comes together)"""
        # Forgot password background slides UP (off-screen top)
        self.forgot_bg_animation.setStartValue(QtCore.QRect(0, 0, 563, 420))
        self.forgot_bg_animation.setEndValue(QtCore.QRect(0, -420, 563, 420))

        # Forgot password frame slides UP (off-screen top)
        self.forgot_frame_animation.setStartValue(QtCore.QRect(131, 20, 301, 380))
        self.forgot_frame_animation.setEndValue(QtCore.QRect(131, -380, 301, 380))

        # Login image slides UP from bottom (comes together)
        self.login_image_animation.setStartValue(QtCore.QRect(0, 420, 281, 421))
        self.login_image_animation.setEndValue(QtCore.QRect(0, 0, 281, 421))

        # Login form slides DOWN from top (comes together from opposite direction)
        self.login_widget_animation.setStartValue(QtCore.QRect(281, -420, 282, 420))
        self.login_widget_animation.setEndValue(QtCore.QRect(281, 0, 282, 420))

        # Start animations
        self.forgot_bg_animation.start()
        self.forgot_frame_animation.start()
        self.login_image_animation.start()
        self.login_widget_animation.start()

    def handle_forgot_password(self):
        """Handle reset password button click"""
        email = self.forgot_email.text().strip()
        new_password = self.forgot_new_password.text()
        confirm_password = self.forgot_confirm_password.text()

        # Call controller
        success, message = AuthController.reset_password(email, new_password, confirm_password)

        if success:
            QMessageBox.information(self.Dialog, "Success ✅",
                                    "Password reset successful!\n\nYou can now login with your new password.")
            # Clear fields
            self.forgot_email.clear()
            self.forgot_new_password.clear()
            self.forgot_confirm_password.clear()
            # Slide back to login
            self.slide_from_forgot_to_login(self.Dialog)
        else:
            QMessageBox.warning(self.Dialog, "Reset Failed ❌", message)

