from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from Model.menu_model import MenuModel


class SalesReportDialog(QDialog):
    """Dialog for displaying weekly, monthly, and yearly sales"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sales Report")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #F5F5F5;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QtWidgets.QLabel("📊 Sales Report")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(title)

        # Tab Widget for different periods
        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #E0E0E0;
                color: #666;
                padding: 10px 20px;
                margin-right: 5px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: red;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #FFCCCC;
            }
        """)

        # Weekly Sales Tab
        weekly_tab = self.create_sales_tab("weekly")
        self.tab_widget.addTab(weekly_tab, "Weekly Sales")

        # Monthly Sales Tab
        monthly_tab = self.create_sales_tab("monthly")
        self.tab_widget.addTab(monthly_tab, "Monthly Sales")

        # Yearly Sales Tab
        yearly_tab = self.create_sales_tab("yearly")
        self.tab_widget.addTab(yearly_tab, "Yearly Sales")

        layout.addWidget(self.tab_widget)

        # Close Button
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()

        close_btn = QtWidgets.QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 30px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #FF4444;
            }
        """)
        close_btn.setFixedHeight(42)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        # Load data
        self.load_sales_data()

    def create_sales_tab(self, period):
        """Create a tab with table for sales data"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)

        # Summary section
        summary_frame = QtWidgets.QFrame()
        summary_frame.setStyleSheet("""
            QFrame {
                background-color: #FFF3F3;
                border: 2px solid red;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        summary_layout = QtWidgets.QHBoxLayout(summary_frame)

        total_orders_label = QtWidgets.QLabel("Total Orders: 0")
        total_orders_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        total_orders_label.setObjectName(f"{period}_orders")

        total_revenue_label = QtWidgets.QLabel("Total Revenue: ₱0.00")
        total_revenue_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        total_revenue_label.setObjectName(f"{period}_revenue")

        summary_layout.addWidget(total_orders_label)
        summary_layout.addStretch()
        summary_layout.addWidget(total_revenue_label)

        layout.addWidget(summary_frame)

        # Table
        table = QTableWidget()
        table.setObjectName(f"{period}_table")

        # Make table non-editable
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        if period == "yearly":
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["Month", "Orders", "Revenue"])
            table.setColumnWidth(0, 250)
            table.setColumnWidth(1, 200)
            table.setColumnWidth(2, 280)
        else:
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["Date", "Orders", "Revenue"])
            table.setColumnWidth(0, 250)
            table.setColumnWidth(1, 200)
            table.setColumnWidth(2, 280)

        table.verticalHeader().setDefaultSectionSize(40)
        table.setStyleSheet("""
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
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F0F0F0;
            }
        """)

        layout.addWidget(table)
        return widget

    def load_sales_data(self):
        """Load sales data for all periods"""
        # Load weekly sales
        weekly_data = MenuModel.get_weekly_sales()
        self.populate_table("weekly", weekly_data)

        # Load monthly sales
        monthly_data = MenuModel.get_monthly_sales()
        self.populate_table("monthly", monthly_data)

        # Load yearly sales
        yearly_data = MenuModel.get_yearly_sales()
        self.populate_table("yearly", yearly_data, is_yearly=True)

    def populate_table(self, period, data, is_yearly=False):
        """Populate table with sales data"""
        table = self.findChild(QTableWidget, f"{period}_table")
        if not table:
            return

        table.setRowCount(len(data))

        total_orders = 0
        total_revenue = 0

        for row, record in enumerate(data):
            # Date/Month column
            if is_yearly:
                date_str = record['sale_month']
            else:
                date_obj = record['sale_date']
                date_str = date_obj.strftime("%b %d, %Y") if date_obj else "N/A"

            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 0, date_item)

            # Orders column
            orders = record['total_orders']
            orders_item = QTableWidgetItem(str(orders))
            orders_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            orders_item.setFlags(orders_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 1, orders_item)

            # Revenue column
            revenue = float(record['total_revenue'])
            revenue_item = QTableWidgetItem(f"₱{revenue:,.2f}")
            revenue_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            revenue_item.setFlags(revenue_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 2, revenue_item)


            total_orders += orders
            total_revenue += revenue

        # Update summary labels
        orders_label = self.findChild(QtWidgets.QLabel, f"{period}_orders")
        revenue_label = self.findChild(QtWidgets.QLabel, f"{period}_revenue")

        if orders_label:
            orders_label.setText(f"Total Orders: {total_orders}")
        if revenue_label:
            revenue_label.setText(f"Total Revenue: ₱{total_revenue:,.2f}")