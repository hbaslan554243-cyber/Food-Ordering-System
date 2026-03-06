from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QLabel, QPushButton, \
    QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit

from Model.menu_model import MenuModel
import os


class CustomerModel:
    """Handles customer-specific database operations"""

    @staticmethod
    def get_user_orders(user_id):
        """Get all orders for a specific user"""
        from Model.database import Database
        connection = Database.get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    o.order_id,
                    o.total_amount,
                    o.status,
                    o.order_date,
                    GROUP_CONCAT(CONCAT(m.name, ' x', oi.quantity) SEPARATOR ', ') as items
                FROM orders o
                JOIN order_items oi ON o.order_id = oi.order_id
                JOIN menu_items m ON oi.menu_id = m.menu_id
                WHERE o.user_id = %s
                GROUP BY o.order_id
                ORDER BY o.order_date DESC
            """
            cursor.execute(query, (user_id,))
            orders = cursor.fetchall()
            return orders
        except Exception as e:
            print(f"❌ Error fetching orders: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def create_order(user_id, cart_items, total_amount, delivery_address, payment_method="Cash on Delivery"):
        """Create a new order"""
        from Model.database import Database
        connection = Database.get_connection()
        if not connection:
            return False, "Database connection failed"

        try:
            cursor = connection.cursor()

            # Insert order
            order_query = """
                INSERT INTO orders (user_id, total_amount, status, delivery_address, payment_method)
                VALUES (%s, %s, 'Pending', %s, %s)
            """
            cursor.execute(order_query, (user_id, total_amount, delivery_address, payment_method))
            order_id = cursor.lastrowid

            # Insert order items
            for item in cart_items:
                item_query = """
                    INSERT INTO order_items (order_id, menu_id, quantity, price)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(item_query, (
                    order_id,
                    item['menu_id'],
                    item['quantity'],
                    item['price']
                ))

                # Update stock
                stock_query = """
                    UPDATE menu_items 
                    SET stock = stock - %s 
                    WHERE menu_id = %s
                """
                cursor.execute(stock_query, (item['quantity'], item['menu_id']))

            connection.commit()
            return True, order_id
        except Exception as e:
            connection.rollback()
            print(f"❌ Error creating order: {e}")
            return False, str(e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def update_user_info(user_id, full_name, phone, address):
        """Update user information"""
        from Model.database import Database
        connection = Database.get_connection()
        if not connection:
            return False, "Database connection failed"

        try:
            cursor = connection.cursor()
            query = """
                UPDATE users 
                SET full_name = %s, phone = %s, address = %s
                WHERE user_id = %s
            """
            cursor.execute(query, (full_name, phone, address, user_id))
            connection.commit()
            return True, "Profile updated successfully"
        except Exception as e:
            connection.rollback()
            print(f"❌ Error updating user: {e}")
            return False, str(e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


class Ui_Dialog(object):
    def __init__(self):
        self.cart_items = []
        self.current_user = None

    def set_user(self, user_data):
        """Set the logged-in user data"""
        self.current_user = user_data
        print(f"✅ User set: {user_data['username']}")

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(909, 518)
        self.Dialog = Dialog

        # ===== EXISTING CODE (Keep everything as is) =====
        self.frame = QtWidgets.QFrame(parent=Dialog)
        self.frame.setGeometry(QtCore.QRect(-20, -10, 941, 80))
        self.frame.setStyleSheet("background-color: white;\n")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setGeometry(QtCore.QRect(30, -3, 85, 80))
        self.label.setText("")
        self.label.setPixmap(
            QtGui.QPixmap(r"C:\Users\keith baslan\Downloads\ChatGPT Image Jan 3, 2026, 07_20_26 PM.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_2.setGeometry(QtCore.QRect(110, 40, 51, 21))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(r"C:\Users\keith baslan\Downloads\Picture2.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        self.pushButton = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton.setGeometry(QtCore.QRect(250, 20, 71, 51))
        self.pushButton.setAutoDefault(False)
        self.pushButton.setStyleSheet("""QPushButton {
    background-color: white;
    color: #666666;
    padding: 12px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 1px;
}
QPushButton:hover {
    background-color: white;
    color: red;
}
QPushButton:pressed {
    background-color: white;
    color: #C0392B;
}""")
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(330, 20, 71, 51))
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setStyleSheet("""QPushButton {
    background-color: white;
    color: #666666;
    padding: 12px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 1px;
}
QPushButton:hover {
    background-color: white;
    color: red;
}
QPushButton:pressed {
    background-color: white;
    color: #C0392B;
}""")
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(405, 20, 100, 51))
        self.pushButton_3.setAutoDefault(False)
        self.pushButton_3.setStyleSheet("""QPushButton {
    background-color: white;
    color: #666666;
    padding: 12px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 1px;
}
QPushButton:hover {
    background-color: white;
    color: red;
}
QPushButton:pressed {
    background-color: white;
    color: #C0392B;
}""")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("CART (0)")


        self.pushButton_4 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(500, 20, 151, 51))
        self.pushButton_4.setAutoDefault(False)
        self.pushButton_4.setStyleSheet("""QPushButton {
    background-color: white;
    color: #666666;
    padding: 12px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 1px;
}
QPushButton:hover {
    background-color: white;
    color: red;
}
QPushButton:pressed {
    background-color: white;
    color: #C0392B;
}""")
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(650, 20, 101, 51))
        self.pushButton_5.setAutoDefault(False)
        self.pushButton_5.setStyleSheet("""QPushButton {
    background-color: white;
    color: #666666;
    padding: 12px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 1px;
}
QPushButton:hover {
    background-color: white;
    color: red;
}
QPushButton:pressed {
    background-color: white;
    color: #C0392B;
}""")
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_6.setGeometry(QtCore.QRect(810, 20, 101, 41))
        self.pushButton_6.setAutoDefault(False)
        self.pushButton_6.setStyleSheet("""QPushButton {
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
    padding: 13px 12px 11px 12px;
}""")
        self.pushButton_6.setObjectName("pushButton_6")

        # HOME PAGE WIDGETS
        self.label_3 = QtWidgets.QLabel(parent=Dialog)
        self.label_3.setGeometry(QtCore.QRect(0, 70, 911, 451))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(r"C:\Users\keith baslan\Downloads\Untitled design (1) (1).png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(parent=Dialog)
        self.label_4.setGeometry(QtCore.QRect(40, 90, 251, 71))
        self.label_4.setStyleSheet("""background-color: none;
    color: white;
    padding: 12px;
    border: none;
    font-size: 30px;
    font-weight: bold;
    letter-spacing: 2px;""")
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(parent=Dialog)
        self.label_5.setGeometry(QtCore.QRect(60, 130, 181, 71))
        self.label_5.setStyleSheet("""background-color: none;
    color: white;
    padding: 12px;
    border: none;
    font-size: 30px;
    font-weight: bold;
    letter-spacing: 2px;""")
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(parent=Dialog)
        self.label_6.setGeometry(QtCore.QRect(30, 170, 271, 71))
        self.label_6.setStyleSheet("""background-color: none;
    color: white;
    padding: 12px;
    border: none;
    font-size: 15px;""")
        self.label_6.setObjectName("label_6")

        self.pushButton_7 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_7.setGeometry(QtCore.QRect(130, 460, 141, 51))
        self.pushButton_7.setAutoDefault(False)
        self.pushButton_7.setStyleSheet("""QPushButton {
    background-color: white;
    color: red;
    border: 2px solid red;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 1px;
}
QPushButton:hover {
    background-color: #FFEBEE;
    border-color: #FF4444;
    color: #FF4444;
    box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
}
QPushButton:pressed {
    background-color: #FFCDD2;
    border-color: #CC0000;
    color: #CC0000;
    padding: 13px 12px 11px 12px;
}""")
        self.pushButton_7.setObjectName("pushButton_7")

        self.label_7 = QtWidgets.QLabel(parent=Dialog)
        self.label_7.setGeometry(QtCore.QRect(50, 240, 281, 41))
        self.label_7.setStyleSheet("""QLabel {
    background-color: #1877F2;
    color: white;
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 13px;
    font-weight: bold;
}""")
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(parent=Dialog)
        self.label_8.setGeometry(QtCore.QRect(90, 290, 281, 41))
        self.label_8.setStyleSheet("""QLabel {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #F58529, stop:0.5 #DD2A7B, stop:1 #8134AF);
    color: white;
    border-radius: 10px;
    padding: 10px 15px;
    font-size: 13px;
    font-weight: bold;
}""")
        self.label_8.setObjectName("label_8")

        self.label_9 = QtWidgets.QLabel(parent=Dialog)
        self.label_9.setGeometry(QtCore.QRect(50, 340, 281, 41))
        self.label_9.setStyleSheet("""QLabel {
    background-color: #000000;
    color: white;
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 13px;
    font-weight: bold;
    border: 1px solid #333333;
}""")
        self.label_9.setObjectName("label_9")

        self.label_10 = QtWidgets.QLabel(parent=Dialog)
        self.label_10.setGeometry(QtCore.QRect(90, 390, 281, 41))
        self.label_10.setStyleSheet("""QLabel {
    background-color: #FFFC00;
    color: black;
    border-radius: 12px;
    padding: 10px 15px;
    font-size: 13px;
    font-weight: bold;
}""")
        self.label_10.setObjectName("label_10")

        # ===== MENU SCROLL AREA =====
        self.menu_scroll = QScrollArea(parent=Dialog)
        self.menu_scroll.setGeometry(QtCore.QRect(0, 70, 909, 448))
        self.menu_scroll.setWidgetResizable(True)
        self.menu_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #F5F5F5;
            }
            QScrollBar:vertical {
                border: none;
                background: #E0E0E0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: red;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #FF4444;
            }
        """)
        self.menu_scroll.hide()

        # ===== CART PAGE =====
        self.cart_widget = QtWidgets.QWidget(parent=Dialog)
        self.cart_widget.setGeometry(QtCore.QRect(0, 70, 909, 448))
        self.cart_widget.setStyleSheet("background-color: white")
        self.cart_widget.hide()

        cart_title = QLabel("Shopping Cart", parent=self.cart_widget)
        cart_title.setGeometry(QtCore.QRect(20, 10, 300, 40))
        cart_title.setStyleSheet("font-size: 28px; font-weight: bold; color: black; background: transparent;")

        self.cart_table = QTableWidget(parent=self.cart_widget)
        self.cart_table.setGeometry(QtCore.QRect(20, 60, 550, 360))
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(["Item", "Price", "Quantity", "Total", "Action"])
        self.cart_table.setColumnWidth(0, 180)
        self.cart_table.setColumnWidth(1, 80)
        self.cart_table.setColumnWidth(2, 110)
        self.cart_table.setColumnWidth(3, 80)
        self.cart_table.setColumnWidth(4, 80)
        self.cart_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                gridline-color: #F0F0F0;
            }
            QHeaderView::section {
                background-color: red;
                color: white;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
                border: none;
            }
        """)

        self.empty_cart_label = QLabel("🛒\n\nYour cart is empty\nAdd items from the menu!", parent=self.cart_widget)
        self.empty_cart_label.setGeometry(QtCore.QRect(20, 150, 550, 100))
        self.empty_cart_label.setStyleSheet("font-size: 18px; color: #999; background: transparent;")
        self.empty_cart_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        summary_frame = QFrame(parent=self.cart_widget)
        summary_frame.setGeometry(QtCore.QRect(590, 25, 300, 400))
        summary_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 12px;
            }
        """)

        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.setContentsMargins(20, 20, 20, 20)
        summary_layout.setSpacing(15)

        summary_title = QLabel("Order Summary")
        summary_title.setStyleSheet("font-size: 20px; font-weight: bold; color: black; background: transparent;")
        summary_layout.addWidget(summary_title)

        subtotal_widget = QtWidgets.QWidget()
        subtotal_layout = QHBoxLayout(subtotal_widget)
        subtotal_layout.setContentsMargins(0, 0, 0, 0)
        subtotal_label = QLabel("Subtotal:")
        subtotal_label.setStyleSheet("font-size: 14px; color: black; background: transparent;")
        self.subtotal_value = QLabel("₱0")
        self.subtotal_value.setStyleSheet("font-size: 14px; font-weight: bold; color: black; background: transparent;")
        self.subtotal_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        subtotal_layout.addWidget(subtotal_label)
        subtotal_layout.addWidget(self.subtotal_value)
        summary_layout.addWidget(subtotal_widget)

        delivery_widget = QtWidgets.QWidget()
        delivery_layout = QHBoxLayout(delivery_widget)
        delivery_layout.setContentsMargins(0, 0, 0, 0)
        delivery_label = QLabel("Delivery Fee:")
        delivery_label.setStyleSheet("font-size: 14px; color: black; background: transparent;")
        self.delivery_value = QLabel("₱50")
        self.delivery_value.setStyleSheet("font-size: 14px; font-weight: bold; color: black; background: transparent;")
        self.delivery_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        delivery_layout.addWidget(delivery_label)
        delivery_layout.addWidget(self.delivery_value)
        summary_layout.addWidget(delivery_widget)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: #E0E0E0;")
        summary_layout.addWidget(divider)

        total_widget = QtWidgets.QWidget()
        total_layout = QHBoxLayout(total_widget)
        total_layout.setContentsMargins(0, 0, 0, 0)
        total_label = QLabel("Total:")
        total_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black; background: transparent;")
        self.total_value = QLabel("₱0")
        self.total_value.setStyleSheet("font-size: 18px; font-weight: bold; color: red; background: transparent;")
        self.total_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_value)
        summary_layout.addWidget(total_widget)

        # Payment Method Section
        payment_label = QLabel("Payment Method:")
        payment_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: black; background: transparent; margin-top: 5px;")
        summary_layout.addWidget(payment_label)

        summary_layout.addSpacing(5)  # Add small space between label and dropdown

        self.payment_method = QtWidgets.QComboBox()
        self.payment_method.addItems([
            "Cash on Delivery",
            "Bank Transfer"
        ])
        self.payment_method.setFixedHeight(40)  # Set a fixed height for the dropdown
        self.payment_method.setStyleSheet("""
            QComboBox {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                background-color: white;
            }
            QComboBox:focus {
                border: 2px solid red;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        summary_layout.addWidget(self.payment_method)

        summary_layout.addSpacing(15)  # Add space before the Proceed to Checkout button

        summary_layout.addStretch()

        self.checkout_btn = QPushButton("🛍️ Proceed to Checkout")
        self.checkout_btn.setAutoDefault(False)
        self.checkout_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF4444;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
            }
        """)
        self.checkout_btn.clicked.connect(self.checkout)
        self.checkout_btn.setEnabled(False)
        summary_layout.addWidget(self.checkout_btn)

        # ===== ORDER HISTORY PAGE =====
        self.history_widget = QtWidgets.QWidget(parent=Dialog)
        self.history_widget.setGeometry(QtCore.QRect(0, 70, 909, 448))
        self.history_widget.setStyleSheet("background-color: white")
        self.history_widget.hide()

        history_title = QLabel("Order History", parent=self.history_widget)
        history_title.setGeometry(QtCore.QRect(20, 10, 300, 40))
        history_title.setStyleSheet("font-size: 28px; font-weight: bold; color: black; background: transparent;")

        self.history_table = QTableWidget(parent=self.history_widget)
        self.history_table.setGeometry(QtCore.QRect(20, 60, 870, 370))
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Order ID", "Date", "Items", "Total", "Status"])
        self.history_table.setColumnWidth(0, 120)
        self.history_table.setColumnWidth(1, 150)
        self.history_table.setColumnWidth(2, 350)
        self.history_table.setColumnWidth(3, 100)
        self.history_table.setColumnWidth(4, 130)
        self.history_table.verticalHeader().setDefaultSectionSize(50)
        self.history_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.history_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.history_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                gridline-color: #F0F0F0;
            }
            QHeaderView::section {
                background-color: red;
                color: white;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
                border: none;
            }
        """)

        # ===== ACCOUNT PAGE =====
        self.account_widget = QtWidgets.QWidget(parent=Dialog)
        self.account_widget.setGeometry(QtCore.QRect(0, 70, 909, 448))

        # Add background image label
        self.account_bg_label = QtWidgets.QLabel(parent=self.account_widget)
        self.account_bg_label.setGeometry(QtCore.QRect(0, 0, 909, 448))
        self.account_bg_label.setPixmap(QtGui.QPixmap(
            r"C:\Users\keith baslan\Downloads\Order your favorites anytime, fast and hassle-free (1).png"))
        self.account_bg_label.setScaledContents(True)
        self.account_bg_label.lower()

        self.account_widget.setStyleSheet("background-color: #F5F5F5;")  # Keep this or remove it
        self.account_widget.hide()

        account_title = QLabel("My Account", parent=self.account_widget)
        account_title.setGeometry(QtCore.QRect(20, 10, 300, 40))
        account_title.setStyleSheet("font-size: 28px; font-weight: bold; color: black; background: transparent;")

        account_frame = QFrame(parent=self.account_widget)
        account_frame.setGeometry(QtCore.QRect(20, 60, 400, 370))
        account_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 12px;
            }
        """)

        # Account Info Form
        self.username_label = QLabel("Username:", parent=account_frame)
        self.username_label.setGeometry(QtCore.QRect(10, 40, 150, 30))
        self.username_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; background: transparent;")

        self.username_value = QLabel("", parent=account_frame)
        self.username_value.setGeometry(QtCore.QRect(170, 40, 221, 30))
        self.username_value.setStyleSheet("font-size: 14px; color: #666; background: transparent;")

        self.email_label = QLabel("Email:", parent=account_frame)
        self.email_label.setGeometry(QtCore.QRect(10, 90, 150, 30))
        self.email_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; background: transparent;")

        self.email_value = QLabel("", parent=account_frame)
        self.email_value.setGeometry(QtCore.QRect(170, 90, 221, 30))
        self.email_value.setStyleSheet("font-size: 14px; color: #666; background: transparent;")

        self.fullname_label = QLabel("Full Name:", parent=account_frame)
        self.fullname_label.setGeometry(QtCore.QRect(10, 140, 150, 30))
        self.fullname_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; background: transparent;")

        self.fullname_input = QLineEdit(parent=account_frame)
        self.fullname_input.setGeometry(QtCore.QRect(170, 140, 221, 35))
        self.fullname_input.setStyleSheet("""
            QLineEdit {
        border: 2px solid #E0E0E0;
        border-radius: 8px;
        padding-left: 8px;
        padding-right: 8px;
        padding-top: 4px;
        padding-bottom: 4px;
        font-size: 13px;
        font-family: Arial;
        background-color: white;
    }
    QLineEdit:focus {
        border: 2px solid red;
    }
""")

        self.phone_label = QLabel("Phone:", parent=account_frame)
        self.phone_label.setGeometry(QtCore.QRect(10, 190, 150, 30))
        self.phone_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; background: transparent;")

        self.phone_input = QLineEdit(parent=account_frame)
        self.phone_input.setGeometry(QtCore.QRect(170, 190, 221, 35))
        self.phone_input.setStyleSheet("""
            QLineEdit {
        border: 2px solid #E0E0E0;
        border-radius: 8px;
        padding-left: 8px;
        padding-right: 8px;
        padding-top: 4px;
        padding-bottom: 4px;
        font-size: 13px;
        font-family: Arial;
        background-color: white;
    }
    QLineEdit:focus {
        border: 2px solid red;
    }
        """)

        self.address_label = QLabel("Address:", parent=account_frame)
        self.address_label.setGeometry(QtCore.QRect(10, 240, 150, 30))
        self.address_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black; background: transparent;")

        self.address_input = QLineEdit(parent=account_frame)
        self.address_input.setGeometry(QtCore.QRect(170, 240, 221, 35))

        self.address_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding-left: 8px;
                padding-right: 8px;
                padding-top: 4px;
                padding-bottom: 4px;
                font-size: 13px;
                font-family: Arial;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid red;
            }
        """)

        self.save_profile_btn = QPushButton("Save Changes", parent=account_frame)
        self.save_profile_btn.setGeometry(QtCore.QRect(120, 300, 150, 40))
        self.save_profile_btn.setAutoDefault(False)
        self.save_profile_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF4444;
            }
        """)
        self.save_profile_btn.clicked.connect(self.save_profile)

        # Connect MENU button to show menu
        self.pushButton_2.clicked.connect(self.show_menu)
        # Connect HOME button to show home
        self.pushButton.clicked.connect(self.show_home)
        # Connect CART button
        self.pushButton_3.clicked.connect(self.show_cart)
        # Connect ORDER HISTORY button
        self.pushButton_4.clicked.connect(self.show_history)
        # Connect ACCOUNT button
        self.pushButton_5.clicked.connect(self.show_account)
        # Connect LOGOUT button
        self.pushButton_6.clicked.connect(self.logout)
        # Connect BROWSE MENU button to show menu
        self.pushButton_7.clicked.connect(self.show_menu)

        # Load menu items from database
        self.load_menu_from_database()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def update_cart_button_text(self):
        """Update cart button to show item count"""
        total_items = sum(item["quantity"] for item in self.cart_items)
        self.pushButton_3.setText(f"CART ({total_items})")

    def show_home(self):
        """Show home page (welcome section)"""
        self.label_3.show()
        self.label_4.show()
        self.label_5.show()
        self.label_6.show()
        self.label_7.show()
        self.label_8.show()
        self.label_9.show()
        self.label_10.show()
        self.pushButton_7.show()
        self.menu_scroll.hide()
        self.cart_widget.hide()
        self.history_widget.hide()
        self.account_widget.hide()

    def show_menu(self):
        """Show menu page"""
        self.label_3.hide()
        self.label_4.hide()
        self.label_5.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.label_9.hide()
        self.label_10.hide()
        self.pushButton_7.hide()
        self.menu_scroll.show()
        self.cart_widget.hide()
        self.history_widget.hide()
        self.account_widget.hide()

    def show_cart(self):
        """Show cart page"""
        self.label_3.hide()
        self.label_4.hide()
        self.label_5.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.label_9.hide()
        self.label_10.hide()
        self.pushButton_7.hide()
        self.menu_scroll.hide()
        self.cart_widget.show()
        self.history_widget.hide()
        self.account_widget.hide()
        self.update_cart_display()

    def show_history(self):
        """Show order history page"""
        self.label_3.hide()
        self.label_4.hide()
        self.label_5.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.label_9.hide()
        self.label_10.hide()
        self.pushButton_7.hide()
        self.menu_scroll.hide()
        self.cart_widget.hide()
        self.history_widget.show()
        self.account_widget.hide()
        self.load_order_history()

    def show_account(self):
        """Show account page"""
        self.label_3.hide()
        self.label_4.hide()
        self.label_5.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.label_9.hide()
        self.label_10.hide()
        self.pushButton_7.hide()
        self.menu_scroll.hide()
        self.cart_widget.hide()
        self.history_widget.hide()
        self.account_widget.show()
        self.load_account_info()

    def load_account_info(self):
        """Load user account information"""
        if self.current_user:
            self.username_value.setText(self.current_user.get('username', 'N/A'))
            self.email_value.setText(self.current_user.get('email', 'N/A'))
            self.fullname_input.setText(self.current_user.get('full_name', ''))
            self.phone_input.setText(self.current_user.get('phone', ''))
            self.address_input.setText(self.current_user.get('address', ''))

    def save_profile(self):
        """Save profile changes"""
        if not self.current_user:
            return

        full_name = self.fullname_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.text().strip()

        success, message = CustomerModel.update_user_info(
            self.current_user['user_id'],
            full_name,
            phone,
            address
        )

        if success:
            # Update current_user data
            self.current_user['full_name'] = full_name
            self.current_user['phone'] = phone
            self.current_user['address'] = address
            QMessageBox.information(None, "Success", message)
        else:
            QMessageBox.warning(None, "Error", message)

    def load_menu_from_database(self):
        """Load menu items from database and organize by category"""
        print("📊 Loading menu from database...")

        # Get all menu items
        items = MenuModel.get_all_menu_items()

        # Organize by category
        categories = {}
        for item in items:
            category = item['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(item)

        # Create scroll content with background image
        # Create scroll content with background image
        scroll_content = QtWidgets.QWidget()
        scroll_content.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)

        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(30)

        # Title
        title = QLabel("Our Menu")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: black;
            background: transparent;
        """)
        scroll_layout.addWidget(title)

        # Create sections for each category
        for category, items_list in categories.items():
            category_section = self.create_category_section(category, items_list)
            scroll_layout.addWidget(category_section)

        scroll_layout.addStretch()
        self.menu_scroll.setWidget(scroll_content)

        print(f"✅ Loaded {len(items)} menu items in {len(categories)} categories")

    def create_category_section(self, category, items):
        """Create a section for each category"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 2px solid #E0E0E0;
            }
        """)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Category header
        header = QLabel(f"🍴 {category}")
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: red;
            background: transparent;
        """)
        layout.addWidget(header)

        # Items grid (4 per row)
        grid_widget = QtWidgets.QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(20)

        for i, item in enumerate(items):
            row = i // 4
            col = i % 4
            card = self.create_menu_card(item)
            grid_layout.addWidget(card, row, col)

        layout.addWidget(grid_widget)
        return section

    def create_menu_card(self, item):
        """Create individual menu item card"""
        card = QFrame()
        card.setFixedSize(180, 240)
        card.setStyleSheet("""
            QFrame {
                background-color: #FAFAFA;
                border: 2px solid #E0E0E0;
                border-radius: 12px;
            }
            QFrame:hover {
                border: 2px solid red;
                background-color: white;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Image
        image_label = QLabel()
        image_label.setFixedSize(160, 100)
        image_label.setStyleSheet("""
            QLabel {
                background-color: #E8E8E8;
                border-radius: 8px;
                border: 1px solid #D0D0D0;
            }
        """)

        if item.get('image_path') and os.path.exists(item['image_path']):
            pixmap = QtGui.QPixmap(item['image_path'])
            scaled_pixmap = pixmap.scaled(
                160, 100,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            image_label.setText("🍔")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setStyleSheet(image_label.styleSheet() + "font-size: 50px;")

        layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Name
        name_label = QLabel(item['name'])
        name_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #333;
            background: transparent;
        """)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setWordWrap(True)
        layout.addWidget(name_label)

        # Price
        price_label = QLabel(f"₱{item['price']:.0f}")
        price_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: red;
            background: transparent;
        """)
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(price_label)

        # Add to cart button
        add_btn = QPushButton("+ Add to Cart")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF4444;
            }
            QPushButton:pressed {
                background-color: #CC0000;
            }
        """)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(lambda checked, i=item: self.add_to_cart(i))
        layout.addWidget(add_btn)

        return card

    def add_to_cart(self, item):
        """Add item to cart"""
        for cart_item in self.cart_items:
            if cart_item["menu_id"] == item["menu_id"]:
                cart_item["quantity"] += 1
                self.update_cart_button_text()
                QMessageBox.information(None, "Added to Cart", f"Quantity updated for {item['name']}")
                return

        self.cart_items.append({
            "menu_id": item["menu_id"],
            "name": item["name"],
            "price": float(item["price"]),
            "quantity": 1
        })
        self.update_cart_button_text()
        QMessageBox.information(None, "Added to Cart", f"{item['name']} added to cart!")

    def update_cart_display(self):
        """Update cart table and summary"""
        self.cart_table.setRowCount(len(self.cart_items))

        subtotal = 0
        for row, item in enumerate(self.cart_items):
            # Item name
            name_item = QTableWidgetItem(item["name"])
            self.cart_table.setItem(row, 0, name_item)

            # Price
            price_item = QTableWidgetItem(f"₱{item['price']:.0f}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.cart_table.setItem(row, 1, price_item)

            # Quantity controls
            qty_widget = QtWidgets.QWidget()
            qty_layout = QHBoxLayout(qty_widget)
            qty_layout.setContentsMargins(5, 0, 5, 0)
            qty_layout.setSpacing(3)

            minus_btn = QPushButton("-")
            minus_btn.setFixedSize(25, 25)
            minus_btn.setStyleSheet("""
                QPushButton {
                    background-color: #E0E0E0;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #D0D0D0; }
            """)
            minus_btn.clicked.connect(lambda checked, r=row: self.decrease_quantity(r))

            qty_label = QLabel(str(item["quantity"]))
            qty_label.setFixedWidth(30)
            qty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            qty_label.setStyleSheet("font-weight: bold; font-size: 14px;")

            plus_btn = QPushButton("+")
            plus_btn.setFixedSize(25, 25)
            plus_btn.setStyleSheet("""
                QPushButton {
                    background-color: red;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #FF4444; }
            """)
            plus_btn.clicked.connect(lambda checked, r=row: self.increase_quantity(r))

            qty_layout.addWidget(minus_btn)
            qty_layout.addWidget(qty_label)
            qty_layout.addWidget(plus_btn)
            self.cart_table.setCellWidget(row, 2, qty_widget)

            # Total
            item_total = item["price"] * item["quantity"]
            total_item = QTableWidgetItem(f"₱{item_total:.0f}")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            total_item.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Weight.Bold))
            self.cart_table.setItem(row, 3, total_item)

            subtotal += item_total

            # Remove button
            remove_widget = QtWidgets.QWidget()
            remove_layout = QHBoxLayout(remove_widget)
            remove_layout.setContentsMargins(0, 0, 0, 0)
            remove_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            remove_btn = QPushButton("🗑️")
            remove_btn.setFixedSize(60, 25)
            remove_btn.setStyleSheet("""
                QPushButton {
                    background-color: red;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                }
                QPushButton:hover { background-color: #C82333; }
            """)
            remove_btn.clicked.connect(lambda checked, r=row: self.remove_from_cart(r))

            remove_layout.addWidget(remove_btn)
            self.cart_table.setCellWidget(row, 4, remove_widget)

        # Update summary
        delivery_fee = 50 if subtotal > 0 else 0
        total = subtotal + delivery_fee

        self.subtotal_value.setText(f"₱{subtotal:.0f}")
        self.delivery_value.setText(f"₱{delivery_fee}")
        self.total_value.setText(f"₱{total:.0f}")

        if len(self.cart_items) == 0:
            self.empty_cart_label.show()
            self.cart_table.hide()
            self.checkout_btn.setEnabled(False)
        else:
            self.empty_cart_label.hide()
            self.cart_table.show()
            self.checkout_btn.setEnabled(True)

    def increase_quantity(self, row):
        if row < len(self.cart_items):
            self.cart_items[row]["quantity"] += 1
            self.update_cart_display()
            self.update_cart_button_text()

    def decrease_quantity(self, row):
        if row < len(self.cart_items):
            if self.cart_items[row]["quantity"] > 1:
                self.cart_items[row]["quantity"] -= 1
                self.update_cart_display()
                self.update_cart_button_text()
            else:
                self.remove_from_cart(row)

    def remove_from_cart(self, row):
        if row < len(self.cart_items):
            item_name = self.cart_items[row]["name"]
            reply = QMessageBox.question(
                None, "Remove Item",
                f"Remove {item_name} from cart?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.cart_items.pop(row)
                self.update_cart_display()
                self.update_cart_button_text()

    def checkout(self):
        """Process checkout"""
        if len(self.cart_items) == 0 or not self.current_user:
            QMessageBox.warning(None, "Cannot Checkout", "Please login to place an order.")
            return

        # Check if user has completed their profile
        if not self.current_user.get('address') or not self.current_user.get('phone'):
            reply = QMessageBox.question(
                None,
                "Incomplete Profile ⚠️",
                "Please complete your profile (address and phone number) before placing an order.\n\n"
                "Would you like to go to your account page now?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.show_account()
            return

        subtotal = sum(item["price"] * item["quantity"] for item in self.cart_items)
        total = subtotal + 50

        delivery_address = self.current_user.get('address', 'No address provided')
        payment_method = self.payment_method.currentText()

        # Handle Bank Transfer payment
        if payment_method == "Bank Transfer":
            bank_info = QMessageBox()
            bank_info.setWindowTitle("Bank Transfer Payment")
            bank_info.setIcon(QMessageBox.Icon.Information)
            bank_info.setText(f"Total Amount to Transfer: ₱{total:.0f}")
            bank_info.setInformativeText(
                "Please transfer to any of these accounts:\n\n"
                "🏦 BDO\n"
                "Account Name: EatoGO Food Services\n"
                "Account Number: 1234-5678-9012\n\n"
                "🏦 BPI\n"
                "Account Name: EatoGO Food Services\n"
                "Account Number: 9876-5432-1098\n\n"
                "⚠️ Your order will be on HOLD until payment is verified.\n"
                "Please send proof of payment to: 0912-345-6789"
            )
            bank_info.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

            if bank_info.exec() == QMessageBox.StandardButton.Cancel:
                return

        # Create order in database
        success, order_id = CustomerModel.create_order(
            self.current_user['user_id'],
            self.cart_items,
            total,
            delivery_address,
            payment_method
        )

        if success:
            if payment_method == "Bank Transfer":
                QMessageBox.information(
                    None, "Order Created! 🏦",
                    f"Order ID: ORD-{order_id:03d}\n"
                    f"Total: ₱{total:.0f}\n\n"
                    f"⚠️ PAYMENT PENDING\n"
                    f"Please transfer ₱{total:.0f} to our bank account\n"
                    f"and send proof of payment with Order ID: ORD-{order_id:03d}\n"
                    f"to 0912-345-6789\n\n"
                    f"Your order will be processed after payment verification."
                )
            else:
                QMessageBox.information(
                    None, "Order Placed! 🎉",
                    f"Order ID: ORD-{order_id:03d}\n"
                    f"Total: ₱{total:.0f}\n\n"
                    f"Your order has been placed successfully!\n"
                    f"15 to 30 minutes upon arrival!\n"
                    f"Track it in Order History."
                )

            self.cart_items.clear()
            self.update_cart_display()
            self.update_cart_button_text()
            self.show_history()
        else:
            QMessageBox.warning(None, "Order Failed", f"Failed to create order: {order_id}")

    def load_order_history(self):
        """Load order history from database"""
        if not self.current_user:
            return

        orders = CustomerModel.get_user_orders(self.current_user['user_id'])

        self.history_table.setRowCount(len(orders))

        for row, order in enumerate(orders):
            # Order ID
            id_item = QTableWidgetItem(f"ORD-{order['order_id']:03d}")
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 0, id_item)

            # Date
            date_str = order['order_date'].strftime("%b %d, %Y") if order['order_date'] else "N/A"
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 1, date_item)

            # Items
            items_item = QTableWidgetItem(order['items'])
            self.history_table.setItem(row, 2, items_item)

            # Total
            total_item = QTableWidgetItem(f"₱{order['total_amount']:.0f}")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 3, total_item)

            # Status
            status_widget = QtWidgets.QWidget()
            status_layout = QHBoxLayout(status_widget)
            status_layout.setContentsMargins(5, 3, 5, 3)

            status_colors = {
                'Completed': ('#D4EDDA', '#155724', '✅'),
                'Processing': ('#FFF3CD', '#856404', '⏳'),
                'Pending': ('#D1ECF1', '#0C5460', '🕒'),
                'Cancelled': ('#F8D7DA', '#721C24', '❌')
            }

            bg_color, text_color, icon = status_colors.get(order['status'], ('#E0E0E0', '#333', '•'))

            status_label = QLabel(f"{icon} {order['status']}")
            status_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {bg_color};
                    color: {text_color};
                    padding: 6px 12px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 11px;
                }}
            """)
            status_layout.addWidget(status_label, alignment=Qt.AlignmentFlag.AlignCenter)
            self.history_table.setCellWidget(row, 4, status_widget)

    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            None, "Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            print("🔒 User logged out")
            self.Dialog.close()

            from View.signINandUP import Ui_Dialog as LoginUI
            self.login_dialog = QtWidgets.QDialog()
            self.login_ui = LoginUI()
            self.login_ui.setupUi(self.login_dialog)
            self.login_dialog.show()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "EatoGO - Customer Dashboard"))
        self.pushButton.setText(_translate("Dialog", "HOME"))
        self.pushButton_2.setText(_translate("Dialog", "MENU"))
        self.pushButton_3.setText(_translate("Dialog", "CART (0)"))
        self.pushButton_4.setText(_translate("Dialog", "ORDER HISTORY"))
        self.pushButton_5.setText(_translate("Dialog", "ACCOUNT"))
        self.pushButton_6.setText(_translate("Dialog", "LOGOUT"))
        self.label_4.setText(_translate("Dialog", "Welcome To"))
        self.label_5.setText(_translate("Dialog", "EatoGO!!!"))
        self.label_6.setText(_translate("Dialog", "delicious food delivired at your door"))
        self.pushButton_7.setText(_translate("Dialog", "BROWSE MENU"))
        self.label_7.setText(_translate("Dialog", " [f] www.facebook.com/EatoGOOfficial"))
        self.label_8.setText(_translate("Dialog", "[@] www.instagram.com/eatogo.official"))
        self.label_9.setText(_translate("Dialog", "          [X]  x.com/EatoGO_Official"))
        self.label_10.setText(_translate("Dialog", "   [☎] (085) 123-4567/ 0912-345-6789"))

