from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
import os
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

        # Print and Close Buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()

        # Export PDF Button
        print_btn = QtWidgets.QPushButton("🖨 Export PDF Report")
        print_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ECC71;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 30px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27AE60;
            }
        """)
        print_btn.setFixedHeight(42)
        print_btn.clicked.connect(self.print_report)
        button_layout.addWidget(print_btn)

        # Close Button
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
        try:
            print("📊 Loading sales data...")

            print("Loading weekly sales...")
            weekly_data = MenuModel.get_weekly_sales()
            print(f"Got {len(weekly_data)} weekly records")
            self.populate_table("weekly", weekly_data)

            print("Loading monthly sales...")
            monthly_data = MenuModel.get_monthly_sales()
            print(f"Got {len(monthly_data)} monthly records")
            self.populate_table("monthly", monthly_data)

            print("Loading yearly sales...")
            yearly_data = MenuModel.get_yearly_sales()
            print(f"Got {len(yearly_data)} yearly records")
            self.populate_table("yearly", yearly_data, is_yearly=True)

            print("✅ Sales data loaded successfully")
        except Exception as e:
            print(f"❌ Error loading sales data: {e}")
            import traceback
            traceback.print_exc()

    def populate_table(self, period, data, is_yearly=False):
        """Populate table with sales data"""
        try:
            table = self.findChild(QTableWidget, f"{period}_table")
            if not table:
                print(f"❌ Table not found: {period}_table")
                return

            if not data:
                table.setRowCount(0)
                print(f"ℹ️ No data for {period} sales")
                return

            table.setRowCount(len(data))

            total_orders = 0
            total_revenue = 0

            for row, record in enumerate(data):
                try:
                    if is_yearly:
                        date_str = str(record.get('sale_month', 'N/A'))
                    else:
                        date_obj = record.get('sale_date')
                        if hasattr(date_obj, 'strftime'):
                            date_str = date_obj.strftime("%b %d, %Y")
                        else:
                            date_str = str(date_obj) if date_obj else "N/A"

                    date_item = QTableWidgetItem(date_str)
                    date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row, 0, date_item)

                    orders = int(record.get('total_orders', 0))
                    orders_item = QTableWidgetItem(str(orders))
                    orders_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row, 1, orders_item)

                    revenue = float(record.get('total_revenue', 0))
                    revenue_item = QTableWidgetItem(f"₱{revenue:,.2f}")
                    revenue_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row, 2, revenue_item)

                    total_orders += orders
                    total_revenue += revenue
                except Exception as e:
                    print(f"❌ Error populating row {row}: {e}")
                    continue

            orders_label = self.findChild(QtWidgets.QLabel, f"{period}_orders")
            revenue_label = self.findChild(QtWidgets.QLabel, f"{period}_revenue")

            if orders_label:
                orders_label.setText(f"Total Orders: {total_orders}")
            if revenue_label:
                revenue_label.setText(f"Total Revenue: ₱{total_revenue:,.2f}")

            print(f"✅ {period} table populated: {len(data)} rows, {total_orders} orders, ₱{total_revenue:,.2f}")

        except Exception as e:
            print(f"❌ Error in populate_table for {period}: {e}")
            import traceback
            traceback.print_exc()

    # ──────────────────────────────────────────────────────────────────────────
    # PDF EXPORT
    # ──────────────────────────────────────────────────────────────────────────

    def print_report(self):
        """Export the current sales tab as a formatted PDF with proper tables"""
        try:
            tab_names   = ["Weekly Sales", "Monthly Sales", "Yearly Sales"]
            period_names = ["weekly", "monthly", "yearly"]
            current_tab_index = self.tab_widget.currentIndex()
            current_period    = period_names[current_tab_index]
            current_tab_name  = tab_names[current_tab_index]

            default_filename = f"EatoGO_{current_tab_name.replace(' ', '_')}_Report.pdf"

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Sales Report as PDF",
                default_filename,
                "PDF Files (*.pdf)"
            )

            if not file_path:
                return  # user cancelled

            self._generate_pdf(file_path, current_period, current_tab_name)

            QMessageBox.information(
                self,
                "Export Successful",
                f"Sales report saved successfully!\n\n{file_path}"
            )

            # Auto-open the PDF
            import subprocess, sys
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", file_path])
            else:
                subprocess.Popen(["xdg-open", file_path])

        except Exception as e:
            print(f"❌ Error exporting PDF: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Export Error", f"Failed to export PDF:\n{str(e)}")

    def _generate_pdf(self, file_path, period, tab_name):
        """Build the PDF using ReportLab with a fully styled table layout"""
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import mm
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from reportlab.platypus import (
            SimpleDocTemplate, Table, TableStyle,
            Paragraph, Spacer, HRFlowable
        )
        from datetime import datetime

        # ── Colour palette ───────────────────────────────────────────────
        RED       = colors.HexColor("#CC0000")
        LIGHT_RED = colors.HexColor("#FFE5E5")
        DARK_GREY = colors.HexColor("#2C3E50")
        MID_GREY  = colors.HexColor("#888888")
        ROW_ALT   = colors.HexColor("#FFF8F8")
        WHITE     = colors.white

        # ── Document setup ───────────────────────────────────────────────
        doc = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
        )
        page_width = A4[0] - 40 * mm

        # ── Styles ───────────────────────────────────────────────────────
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontSize=22,
            textColor=DARK_GREY,
            spaceAfter=4,
            alignment=TA_LEFT,
        )
        subtitle_style = ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            fontSize=14,
            textColor=RED,
            fontName="Helvetica-Bold",
            spaceAfter=2,
            alignment=TA_LEFT,
        )
        meta_style = ParagraphStyle(
            "Meta",
            parent=styles["Normal"],
            fontSize=9,
            textColor=MID_GREY,
            spaceAfter=0,
            alignment=TA_LEFT,
        )
        summary_label_style = ParagraphStyle(
            "SummaryLabel",
            parent=styles["Normal"],
            fontSize=11,
            textColor=DARK_GREY,
            fontName="Helvetica-Bold",
        )
        summary_value_style = ParagraphStyle(
            "SummaryValue",
            parent=styles["Normal"],
            fontSize=11,
            textColor=RED,
            fontName="Helvetica-Bold",
            alignment=TA_LEFT,
        )
        no_data_style = ParagraphStyle(
            "NoData",
            parent=styles["Normal"],
            fontSize=11,
            textColor=MID_GREY,
            alignment=TA_CENTER,
            spaceBefore=20,
        )
        footer_style = ParagraphStyle(
            "Footer",
            parent=styles["Normal"],
            fontSize=8,
            textColor=MID_GREY,
            alignment=TA_CENTER,
            spaceBefore=4,
        )

        # ── Collect data from widget ─────────────────────────────────────
        table_widget  = self.findChild(QTableWidget, f"{period}_table")
        orders_label  = self.findChild(QtWidgets.QLabel, f"{period}_orders")
        revenue_label = self.findChild(QtWidgets.QLabel, f"{period}_revenue")

        total_orders_text  = orders_label.text()  if orders_label  else "Total Orders: 0"
        total_revenue_text = revenue_label.text() if revenue_label else "Total Revenue: P0.00"

        # Replace peso sign with plain text so ReportLab doesn't choke on it
        total_revenue_text = total_revenue_text.replace("₱", "PHP ")

        is_yearly   = (period == "yearly")
        col0_header = "Month" if is_yearly else "Date"
        headers     = [col0_header, "Orders", "Revenue"]

        rows = []
        if table_widget:
            for r in range(table_widget.rowCount()):
                row_data = []
                for c in range(3):
                    item = table_widget.item(r, c)
                    cell_text = (item.text() if item else "")
                    # Replace peso sign for safe rendering
                    cell_text = cell_text.replace("₱", "PHP ")
                    row_data.append(cell_text)
                rows.append(row_data)

        # ── Build PDF story ──────────────────────────────────────────────
        story = []

        # Header
        story.append(Paragraph("EatoGO", title_style))
        story.append(Paragraph(f"Sales Report  —  {tab_name}", subtitle_style))
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y   %I:%M %p')}",
            meta_style
        ))
        story.append(HRFlowable(
            width="100%", thickness=2, color=RED,
            spaceAfter=12, spaceBefore=6
        ))

        # Summary card (two-column table)
        summary_table_data = [[
            Paragraph(total_orders_text,  summary_label_style),
            Paragraph(total_revenue_text, summary_value_style),
        ]]
        summary_tbl = Table(
            summary_table_data,
            colWidths=[page_width * 0.5, page_width * 0.5]
        )
        summary_tbl.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, -1), LIGHT_RED),
            ("BOX",          (0, 0), (-1, -1), 1.5, RED),
            ("LEFTPADDING",  (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING",   (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(summary_tbl)
        story.append(Spacer(1, 16))

        # Main data table
        if rows:
            col_widths = [page_width * 0.42, page_width * 0.24, page_width * 0.34]
            table_data = [headers] + rows

            # Build alternating row background styles
            alt_row_styles = []
            for i in range(1, len(table_data)):
                bg = WHITE if i % 2 == 1 else ROW_ALT
                alt_row_styles.append(("BACKGROUND", (0, i), (-1, i), bg))

            main_tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
            main_tbl.setStyle(TableStyle([
                # ── Header row ──────────────────────────────────────────
                ("BACKGROUND",    (0, 0), (-1, 0), RED),
                ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
                ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE",      (0, 0), (-1, 0), 11),
                ("ALIGN",         (0, 0), (-1, 0), "CENTER"),
                ("TOPPADDING",    (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

                # ── Data rows ───────────────────────────────────────────
                ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE",      (0, 1), (-1, -1), 10),
                ("ALIGN",         (0, 1), (0,  -1), "LEFT"),   # Date col left
                ("ALIGN",         (1, 1), (-1, -1), "CENTER"), # Others centre
                ("LEFTPADDING",   (0, 1), (0,  -1), 10),
                ("TOPPADDING",    (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
                ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),

                # ── Grid & border ────────────────────────────────────────
                ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
                ("BOX",           (0, 0), (-1, -1), 1.5, RED),
                ("LINEBELOW",     (0, 0), (-1, 0),  1.5, RED),  # thick header bottom

                # ── Alternating rows ─────────────────────────────────────
                *alt_row_styles,
            ]))

            story.append(main_tbl)

        else:
            story.append(Paragraph("No sales data available for this period.", no_data_style))

        # Footer
        story.append(Spacer(1, 20))
        story.append(HRFlowable(width="100%", thickness=0.5, color=MID_GREY))
        story.append(Paragraph(
            "EatoGO Administration System  •  Confidential",
            footer_style
        ))

        doc.build(story)
        print(f"✅ PDF saved to {file_path}")


# ══════════════════════════════════════════════════════════════════════════════
# AddMenuDialog
# ══════════════════════════════════════════════════════════════════════════════

class AddMenuDialog(QDialog):
    """Dialog for adding new menu items"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Menu Item")
        self.setFixedSize(450, 580)
        self.setStyleSheet("background-color: #F5F5F5;")

        self.selected_image_path = None

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QtWidgets.QLabel("+ Add New Menu Item")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(title)

        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setVerticalSpacing(15)

        self.category_input = QtWidgets.QComboBox()
        self.category_input.addItems(["Burgers", "Pizza", "Pasta", "Desserts", "Drinks", "Meals"])
        self.category_input.setStyleSheet(self.get_input_style())
        self.category_input.setFixedHeight(40)
        form_layout.addRow("Category:", self.category_input)

        self.food_name_input = QtWidgets.QLineEdit()
        self.food_name_input.setPlaceholderText("Enter food name")
        self.food_name_input.setStyleSheet(self.get_input_style())
        self.food_name_input.setFixedHeight(40)
        form_layout.addRow("Food Name:", self.food_name_input)

        self.price_input = QtWidgets.QLineEdit()
        self.price_input.setPlaceholderText("₱0.00")
        self.price_input.setStyleSheet(self.get_input_style())
        self.price_input.setFixedHeight(40)
        form_layout.addRow("Price:", self.price_input)

        self.stock_input = QtWidgets.QSpinBox()
        self.stock_input.setRange(0, 1000)
        self.stock_input.setValue(100)
        self.stock_input.setStyleSheet(self.get_input_style())
        self.stock_input.setFixedHeight(40)
        form_layout.addRow("Stock:", self.stock_input)

        layout.addLayout(form_layout)
        layout.addSpacing(10)

        image_section = QtWidgets.QFrame()
        image_section.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
            }
        """)
        image_layout = QtWidgets.QVBoxLayout(image_section)
        image_layout.setContentsMargins(15, 15, 15, 15)
        image_layout.setSpacing(10)

        self.preview_container = QtWidgets.QFrame()
        self.preview_container.setFixedSize(200, 150)
        self.preview_container.setStyleSheet("""
            QFrame {
                border: 2px dashed #CCCCCC;
                border-radius: 8px;
                background-color: #F9F9F9;
            }
        """)

        preview_layout = QtWidgets.QVBoxLayout(self.preview_container)
        preview_layout.setContentsMargins(5, 5, 5, 5)

        self.image_preview = QtWidgets.QLabel()
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setText("📷\nNo Image Selected")
        self.image_preview.setStyleSheet("border: none; background: transparent; font-size: 11px; color: #999;")
        self.image_preview.setWordWrap(True)
        preview_layout.addWidget(self.image_preview)

        image_layout.addWidget(self.preview_container, alignment=Qt.AlignmentFlag.AlignCenter)

        self.upload_btn = QtWidgets.QPushButton("🖼 Browse Image")
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #FF4444;
            }
        """)
        self.upload_btn.setFixedHeight(38)
        self.upload_btn.clicked.connect(self.upload_image)
        image_layout.addWidget(self.upload_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(image_section)
        layout.addStretch()

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95A5A6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 30px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7F8C8D;
            }
        """)
        cancel_btn.setFixedHeight(42)
        cancel_btn.clicked.connect(self.reject)

        save_btn = QtWidgets.QPushButton("Add Item")
        save_btn.setStyleSheet("""
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
        save_btn.setFixedHeight(42)
        save_btn.clicked.connect(self.accept)

        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

    def get_input_style(self):
        return """
            QLineEdit, QComboBox, QSpinBox {
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 2px solid red;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
        """

    def upload_image(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(
            self, "Select Food Image", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if image_path:
            self.selected_image_path = image_path
            pixmap = QtGui.QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(
                190, 140,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_preview.setPixmap(scaled_pixmap)
            self.image_preview.setText("")
            self.preview_container.setStyleSheet("""
                QFrame {
                    border: 2px solid #2ECC71;
                    border-radius: 8px;
                    background-color: white;
                }
            """)

    def get_data(self):
        return {
            'category':   self.category_input.currentText(),
            'name':       self.food_name_input.text(),
            'price':      self.price_input.text(),
            'stock':      self.stock_input.value(),
            'image_path': self.selected_image_path,
        }


# ══════════════════════════════════════════════════════════════════════════════
# EditMenuDialog
# ══════════════════════════════════════════════════════════════════════════════

class EditMenuDialog(QDialog):
    """Dialog for editing menu items"""

    def __init__(self, parent=None, menu_id=None, category="", name="",
                 price="", stock=0, image_path=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Menu Item")
        self.setFixedSize(450, 580)
        self.setStyleSheet("background-color: #F5F5F5;")

        self.menu_id = menu_id
        self.selected_image_path = image_path

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QtWidgets.QLabel("✏️ Edit Menu Item")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(title)

        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setVerticalSpacing(15)

        self.category_input = QtWidgets.QComboBox()
        self.category_input.addItems(["Burgers", "Pizza", "Pasta", "Desserts", "Drinks", "Meals"])
        self.category_input.setCurrentText(category)
        self.category_input.setStyleSheet(self.get_input_style())
        self.category_input.setFixedHeight(40)
        form_layout.addRow("Category:", self.category_input)

        self.food_name_input = QtWidgets.QLineEdit()
        self.food_name_input.setPlaceholderText("Enter food name")
        self.food_name_input.setText(name)
        self.food_name_input.setStyleSheet(self.get_input_style())
        self.food_name_input.setFixedHeight(40)
        form_layout.addRow("Food Name:", self.food_name_input)

        self.price_input = QtWidgets.QLineEdit()
        self.price_input.setPlaceholderText("₱0.00")
        self.price_input.setText(price)
        self.price_input.setStyleSheet(self.get_input_style())
        self.price_input.setFixedHeight(40)
        form_layout.addRow("Price:", self.price_input)

        self.stock_input = QtWidgets.QSpinBox()
        self.stock_input.setRange(0, 1000)
        self.stock_input.setValue(int(stock))
        self.stock_input.setStyleSheet(self.get_input_style())
        self.stock_input.setFixedHeight(40)
        form_layout.addRow("Stock:", self.stock_input)

        layout.addLayout(form_layout)
        layout.addSpacing(10)

        image_section = QtWidgets.QFrame()
        image_section.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
            }
        """)
        image_layout = QtWidgets.QVBoxLayout(image_section)
        image_layout.setContentsMargins(15, 15, 15, 15)
        image_layout.setSpacing(10)

        self.preview_container = QtWidgets.QFrame()
        self.preview_container.setFixedSize(200, 150)
        self.preview_container.setStyleSheet("""
            QFrame {
                border: 2px dashed #CCCCCC;
                border-radius: 8px;
                background-color: #F9F9F9;
            }
        """)

        preview_layout = QtWidgets.QVBoxLayout(self.preview_container)
        preview_layout.setContentsMargins(5, 5, 5, 5)

        self.image_preview = QtWidgets.QLabel()
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setText("📷\nNo Image Selected")
        self.image_preview.setStyleSheet("border: none; background: transparent; font-size: 11px; color: #999;")
        self.image_preview.setWordWrap(True)
        preview_layout.addWidget(self.image_preview)

        image_layout.addWidget(self.preview_container, alignment=Qt.AlignmentFlag.AlignCenter)

        if image_path and os.path.exists(image_path):
            pixmap = QtGui.QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(
                190, 140,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_preview.setPixmap(scaled_pixmap)
            self.image_preview.setText("")
            self.preview_container.setStyleSheet("""
                QFrame {
                    border: 2px solid #2ECC71;
                    border-radius: 8px;
                    background-color: white;
                }
            """)

        self.upload_btn = QtWidgets.QPushButton("🖼 Browse Image")
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #FF4444;
            }
        """)
        self.upload_btn.setFixedHeight(38)
        self.upload_btn.clicked.connect(self.upload_image)
        image_layout.addWidget(self.upload_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(image_section)
        layout.addStretch()

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95A5A6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 30px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7F8C8D;
            }
        """)
        cancel_btn.setFixedHeight(42)
        cancel_btn.clicked.connect(self.reject)

        save_btn = QtWidgets.QPushButton("Update Item")
        save_btn.setStyleSheet("""
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
        save_btn.setFixedHeight(42)
        save_btn.clicked.connect(self.accept)

        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

    def get_input_style(self):
        return """
            QLineEdit, QComboBox, QSpinBox {
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 2px solid red;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
        """

    def upload_image(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(
            self, "Select Food Image", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if image_path:
            self.selected_image_path = image_path
            pixmap = QtGui.QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(
                190, 140,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_preview.setPixmap(scaled_pixmap)
            self.image_preview.setText("")
            self.preview_container.setStyleSheet("""
                QFrame {
                    border: 2px solid #2ECC71;
                    border-radius: 8px;
                    background-color: white;
                }
            """)

    def get_data(self):
        return {
            'menu_id':    self.menu_id,
            'category':   self.category_input.currentText(),
            'name':       self.food_name_input.text(),
            'price':      self.price_input.text(),
            'stock':      self.stock_input.value(),
            'image_path': self.selected_image_path,
        }


# ══════════════════════════════════════════════════════════════════════════════
# Main Admin UI
# ══════════════════════════════════════════════════════════════════════════════

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(900, 531)
        Dialog.setFixedSize(900, 531)
        Dialog.setStyleSheet("background-color: #F5F5F5;")

        # Sidebar Frame
        self.frame = QtWidgets.QFrame(parent=Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 161, 531))
        self.frame.setStyleSheet("background-color: white;")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        # Logo
        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 81, 81))
        self.label.setText("")
        logo_path = r"C:\Users\keith baslan\Downloads\ChatGPT Image Jan 3, 2026, 07_20_26 PM.png"
        if os.path.exists(logo_path):
            self.label.setPixmap(QtGui.QPixmap(logo_path))
            self.label.setScaledContents(True)
        else:
            self.label.setText("🍔")
            self.label.setStyleSheet("font-size: 50px;")
            self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_2.setGeometry(QtCore.QRect(80, 40, 61, 21))
        self.label_2.setText("")
        text_logo_path = r"C:\Users\keith baslan\Downloads\Picture2.png"
        if os.path.exists(text_logo_path):
            self.label_2.setPixmap(QtGui.QPixmap(text_logo_path))
            self.label_2.setScaledContents(True)
        else:
            self.label_2.setText("EatoGO")
            self.label_2.setStyleSheet("font-size: 14px; font-weight: bold; color: red;")
        self.label_2.setObjectName("label_2")

        # Navigation Buttons
        nav_btn_style = """
QPushButton {
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
    background-color: red;
    color: white;
}
QPushButton:pressed {
    background-color: #C0392B;
    color: white;
}
"""
        self.pushButton = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton.setGeometry(QtCore.QRect(0, 90, 161, 41))
        self.pushButton.setAutoDefault(False)
        self.pushButton.setStyleSheet(nav_btn_style)
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 140, 161, 41))
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setStyleSheet(nav_btn_style)
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 190, 161, 41))
        self.pushButton_3.setAutoDefault(False)
        self.pushButton_3.setStyleSheet(nav_btn_style)
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(0, 240, 161, 41))
        self.pushButton_4.setAutoDefault(False)
        self.pushButton_4.setStyleSheet(nav_btn_style)
        self.pushButton_4.setObjectName("pushButton_4")

        # Logout Button
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 460, 121, 41))
        self.pushButton_5.setAutoDefault(False)
        self.pushButton_5.setStyleSheet("""
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
}
QPushButton:pressed {
    background-color: #CC0000;
}
""")
        self.pushButton_5.setObjectName("pushButton_5")

        # Stacked Widget
        self.stackedWidget = QtWidgets.QStackedWidget(parent=Dialog)
        self.stackedWidget.setGeometry(QtCore.QRect(161, 0, 739, 531))
        self.stackedWidget.setObjectName("stackedWidget")

        self.create_dashboard_page()
        self.create_orders_page()
        self.create_menu_page()
        self.create_customers_page()

        self.retranslateUi(Dialog)
        self.setup_connections(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.stackedWidget.setCurrentIndex(0)

        self.load_menu_items()
        self.load_dashboard_stats()
        self.load_customers()
        self.load_orders()

    def get_table_style(self):
        return """
QTableView, QTableWidget {
    background-color: white;
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    gridline-color: #F0F0F0;
    selection-background-color: #FFE5E5;
}
QHeaderView::section {
    background-color: red;
    color: white;
    padding: 12px;
    font-weight: bold;
    font-size: 12px;
    border: none;
    border-right: 1px solid #CC0000;
}
QHeaderView::section:last {
    border-right: none;
}
QTableView::item, QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #F0F0F0;
}
QTableView::item:selected, QTableWidget::item:selected {
    background-color: #FFE5E5;
    color: black;
}
"""

    def create_dashboard_page(self):
        page = QtWidgets.QWidget()

        frame_2 = QtWidgets.QFrame(parent=page)
        frame_2.setGeometry(QtCore.QRect(10, 10, 171, 61))
        frame_2.setStyleSheet("background-color: white;")
        frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        label_5 = QtWidgets.QLabel(parent=frame_2)
        label_5.setGeometry(QtCore.QRect(10, 10, 141, 21))
        label_5.setStyleSheet("color: black; font-size: 15px; font-weight: bold; background-color: transparent;")
        label_5.setText("DASHBOARD")

        label_6 = QtWidgets.QLabel(parent=frame_2)
        label_6.setGeometry(QtCore.QRect(10, 30, 161, 20))
        label_6.setStyleSheet("color: grey; font-size: 12px; font-weight: 600; background-color: transparent;")
        label_6.setText("Welcome Administrator!!!")

        self.sales_report_btn = QtWidgets.QPushButton(parent=page)
        self.sales_report_btn.setGeometry(QtCore.QRect(570, 20, 150, 40))
        self.sales_report_btn.setText("📊 Sales Report")
        self.sales_report_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #FF4444; }
            QPushButton:pressed { background-color: #CC0000; }
        """)
        self.sales_report_btn.clicked.connect(self.show_sales_report)

        horizontalLayoutWidget = QtWidgets.QWidget(parent=page)
        horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 90, 720, 150))
        horizontalLayout = QtWidgets.QHBoxLayout(horizontalLayoutWidget)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalLayout.setSpacing(15)

        labels = ["Total Menu", "Total Revenue", "Total Orders", "Total Customers"]
        self.stat_cards = []
        for label in labels:
            card_container = QtWidgets.QWidget()
            card_layout = QtWidgets.QVBoxLayout(card_container)
            card_layout.setContentsMargins(0, 0, 0, 0)
            card_layout.setSpacing(10)

            card = QtWidgets.QLabel()
            card.setStyleSheet("QLabel { background: red; color: white; border-radius: 10px; }")
            card.setText("0")
            card.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card.setFont(QtGui.QFont("Arial", 30, QtGui.QFont.Weight.Bold))
            card.setFixedHeight(100)

            label_widget = QtWidgets.QLabel(label)
            label_widget.setStyleSheet("color: #333; font-size: 12px; font-weight: 600; background-color: transparent;")
            label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

            card_layout.addWidget(card)
            card_layout.addWidget(label_widget)
            horizontalLayout.addWidget(card_container)
            self.stat_cards.append(card)

        label_9 = QtWidgets.QLabel(parent=page)
        label_9.setGeometry(QtCore.QRect(10, 250, 250, 21))
        label_9.setStyleSheet("color: black; font-size: 15px; font-weight: bold; background-color: transparent;")
        label_9.setText("SALES OVERVIEW")

        self.sales_table = QTableWidget(parent=page)
        self.sales_table.setGeometry(QtCore.QRect(10, 280, 720, 241))
        self.sales_table.setColumnCount(4)
        self.sales_table.setHorizontalHeaderLabels(["Menu Item", "Category", "Number of Sales", "Total Revenue"])
        self.sales_table.setColumnWidth(0, 250)
        self.sales_table.setColumnWidth(1, 150)
        self.sales_table.setColumnWidth(2, 150)
        self.sales_table.setColumnWidth(3, 150)
        self.sales_table.verticalHeader().setDefaultSectionSize(40)
        self.sales_table.setStyleSheet(self.get_table_style())

        self.stackedWidget.addWidget(page)

    def create_orders_page(self):
        page = QtWidgets.QWidget()

        frame_2 = QtWidgets.QFrame(parent=page)
        frame_2.setGeometry(QtCore.QRect(10, 10, 171, 61))
        frame_2.setStyleSheet("background-color: white;")
        frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        label_5 = QtWidgets.QLabel(parent=frame_2)
        label_5.setGeometry(QtCore.QRect(10, 10, 141, 21))
        label_5.setStyleSheet("color: black; font-size: 15px; font-weight: bold; background-color: transparent;")
        label_5.setText("ORDERS")

        label_6 = QtWidgets.QLabel(parent=frame_2)
        label_6.setGeometry(QtCore.QRect(10, 30, 161, 20))
        label_6.setStyleSheet("color: grey; font-size: 12px; font-weight: 600; background-color: transparent;")
        label_6.setText("Welcome Administrator!!!")

        label_7 = QtWidgets.QLabel(parent=page)
        label_7.setGeometry(QtCore.QRect(20, 70, 371, 41))
        label_7.setStyleSheet("color: black; font-size: 25px; font-weight: bold; letter-spacing: 2px; background-color: transparent;")
        label_7.setText("ORDERS MANAGEMENT")

        self.orders_table = QtWidgets.QTableView(parent=page)
        self.orders_table.setGeometry(QtCore.QRect(20, 120, 700, 371))
        self.orders_table.setStyleSheet(self.get_table_style())

        self.stackedWidget.addWidget(page)

    def create_menu_page(self):
        page = QtWidgets.QWidget()

        frame_2 = QtWidgets.QFrame(parent=page)
        frame_2.setGeometry(QtCore.QRect(10, 10, 171, 61))
        frame_2.setStyleSheet("background-color: white;")
        frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        label_5 = QtWidgets.QLabel(parent=frame_2)
        label_5.setGeometry(QtCore.QRect(10, 10, 141, 21))
        label_5.setStyleSheet("color: black; font-size: 15px; font-weight: bold; background-color: transparent;")
        label_5.setText("MENU")

        label_6 = QtWidgets.QLabel(parent=frame_2)
        label_6.setGeometry(QtCore.QRect(10, 30, 161, 20))
        label_6.setStyleSheet("color: grey; font-size: 12px; font-weight: 600; background-color: transparent;")
        label_6.setText("Welcome Administrator!!!")

        label_7 = QtWidgets.QLabel(parent=page)
        label_7.setGeometry(QtCore.QRect(20, 70, 371, 41))
        label_7.setStyleSheet("color: black; font-size: 25px; font-weight: bold; letter-spacing: 2px; background-color: transparent;")
        label_7.setText("MENU MANAGEMENT")

        self.add_menu_btn = QtWidgets.QPushButton(parent=page)
        self.add_menu_btn.setGeometry(QtCore.QRect(580, 75, 140, 35))
        self.add_menu_btn.setAutoDefault(False)
        self.add_menu_btn.setStyleSheet("""
QPushButton {
    background-color: red; color: white; border: none;
    border-radius: 8px; padding: 8px; font-size: 13px; font-weight: bold;
}
QPushButton:hover { background-color: #FF4444; }
QPushButton:pressed { background-color: #CC0000; }
""")
        self.add_menu_btn.setText("+ Add New Item")

        self.search_input = QtWidgets.QLineEdit(parent=page)
        self.search_input.setGeometry(QtCore.QRect(400, 75, 170, 35))
        self.search_input.setPlaceholderText("Search menu...")
        self.search_input.setStyleSheet("""
QLineEdit {
    border: 2px solid #E0E0E0; border-radius: 8px;
    padding: 8px 12px; font-size: 13px; background-color: white;
}
QLineEdit:focus { border: 2px solid red; }
""")
        self.search_input.textChanged.connect(self.search_menu)

        self.menu_table = QTableWidget(parent=page)
        self.menu_table.setGeometry(QtCore.QRect(20, 120, 700, 391))
        self.menu_table.setColumnCount(6)
        self.menu_table.setHorizontalHeaderLabels(["Image", "Category", "Name", "Price", "Stock", "Actions"])
        self.menu_table.setColumnWidth(0, 100)
        self.menu_table.setColumnWidth(1, 100)
        self.menu_table.setColumnWidth(2, 180)
        self.menu_table.setColumnWidth(3, 80)
        self.menu_table.setColumnWidth(4, 80)
        self.menu_table.setColumnWidth(5, 140)
        self.menu_table.verticalHeader().setDefaultSectionSize(90)
        self.menu_table.setStyleSheet(self.get_table_style() + "QTableWidget::item { padding: 5px; }")

        self.stackedWidget.addWidget(page)

    def create_customers_page(self):
        page = QtWidgets.QWidget()

        frame_2 = QtWidgets.QFrame(parent=page)
        frame_2.setGeometry(QtCore.QRect(10, 10, 171, 61))
        frame_2.setStyleSheet("background-color: white;")
        frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        label_5 = QtWidgets.QLabel(parent=frame_2)
        label_5.setGeometry(QtCore.QRect(10, 10, 141, 21))
        label_5.setStyleSheet("color: black; font-size: 15px; font-weight: bold; background-color: transparent;")
        label_5.setText("CUSTOMERS")

        label_6 = QtWidgets.QLabel(parent=frame_2)
        label_6.setGeometry(QtCore.QRect(10, 30, 161, 20))
        label_6.setStyleSheet("color: grey; font-size: 12px; font-weight: 600; background-color: transparent;")
        label_6.setText("Welcome Administrator!!!")

        label_7 = QtWidgets.QLabel(parent=page)
        label_7.setGeometry(QtCore.QRect(20, 70, 431, 41))
        label_7.setStyleSheet("color: black; font-size: 25px; font-weight: bold; letter-spacing: 2px; background-color: transparent;")
        label_7.setText("CUSTOMERS MANAGEMENT")

        self.customers_table = QTableWidget(parent=page)
        self.customers_table.setGeometry(QtCore.QRect(20, 120, 700, 391))
        self.customers_table.setColumnCount(5)
        self.customers_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.customers_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.customers_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.customers_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.customers_table.verticalHeader().setDefaultSectionSize(40)
        self.customers_table.verticalHeader().setFixedWidth(50)
        self.customers_table.setHorizontalHeaderLabels(["Username", "Email", "Phone", "Address", "Total Spent"])
        self.customers_table.setColumnWidth(0, 120)
        self.customers_table.setColumnWidth(1, 180)
        self.customers_table.setColumnWidth(2, 100)
        self.customers_table.setColumnWidth(3, 180)
        self.customers_table.setColumnWidth(4, 120)
        self.customers_table.setStyleSheet(self.get_table_style())

        self.stackedWidget.addWidget(page)

    def setup_connections(self, Dialog):
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_2.clicked.connect(lambda: [self.stackedWidget.setCurrentIndex(1), self.load_orders()])
        self.pushButton_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButton_4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.pushButton_5.clicked.connect(lambda: self.logout(Dialog))
        self.add_menu_btn.clicked.connect(lambda: self.open_add_menu_dialog(Dialog))

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "EatoGO - Admin Dashboard"))
        self.pushButton.setText(_translate("Dialog", "DASHBOARD"))
        self.pushButton_2.setText(_translate("Dialog", "ORDERS"))
        self.pushButton_3.setText(_translate("Dialog", "MENU"))
        self.pushButton_4.setText(_translate("Dialog", "CUSTOMERS"))
        self.pushButton_5.setText(_translate("Dialog", "LOGOUT"))

    # ── Menu helpers ──────────────────────────────────────────────────────────

    def search_menu(self):
        search_text = self.search_input.text().lower()
        for row in range(self.menu_table.rowCount()):
            name_item     = self.menu_table.item(row, 2)
            category_item = self.menu_table.item(row, 1)
            name_match     = name_item     and search_text in name_item.text().lower()
            category_match = category_item and search_text in category_item.text().lower()
            self.menu_table.setRowHidden(row, not (search_text == "" or name_match or category_match))

    def add_item_to_menu_table(self, image_path, category, name, price, stock, menu_id=None):
        row = self.menu_table.rowCount()
        self.menu_table.insertRow(row)

        # Image
        if image_path and os.path.exists(image_path):
            image_label = QtWidgets.QLabel()
            pixmap = QtGui.QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setStyleSheet("QLabel { border: 1px solid #E0E0E0; border-radius: 6px; padding: 3px; background-color: white; }")
            self.menu_table.setCellWidget(row, 0, image_label)
        else:
            placeholder = QtWidgets.QLabel("🖼️")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setStyleSheet("font-size: 32px; color: #CCC;")
            self.menu_table.setCellWidget(row, 0, placeholder)

        category_item = QTableWidgetItem(str(category))
        category_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.menu_table.setItem(row, 1, category_item)

        name_item = QTableWidgetItem(str(name))
        name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.menu_table.setItem(row, 2, name_item)

        price_item = QTableWidgetItem(str(price))
        price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.menu_table.setItem(row, 3, price_item)

        stock_item = QTableWidgetItem(str(stock))
        stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.menu_table.setItem(row, 4, stock_item)

        if menu_id:
            name_item.setData(Qt.ItemDataRole.UserRole, menu_id)

        action_widget = QtWidgets.QWidget()
        action_layout = QtWidgets.QHBoxLayout(action_widget)
        action_layout.setContentsMargins(5, 5, 5, 5)
        action_layout.setSpacing(5)

        edit_btn = QtWidgets.QPushButton("Edit")
        edit_btn.setStyleSheet("""
            QPushButton { background-color: #3498db; color: white; border: none;
                border-radius: 5px; padding: 6px 10px; font-size: 11px; font-weight: bold; }
            QPushButton:hover { background-color: #5DADE2; }
        """)
        edit_btn.clicked.connect(lambda checked, r=row: self.edit_menu_item(r))

        delete_btn = QtWidgets.QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton { background-color: red; color: white; border: none;
                border-radius: 5px; padding: 6px 10px; font-size: 11px; font-weight: bold; }
            QPushButton:hover { background-color: #FF4444; }
        """)
        delete_btn.clicked.connect(lambda checked, r=row: self.delete_menu_item(r))

        action_layout.addStretch()
        action_layout.addWidget(edit_btn)
        action_layout.addWidget(delete_btn)
        action_layout.addStretch()
        self.menu_table.setCellWidget(row, 5, action_widget)

    def delete_menu_item(self, row):
        name_item = self.menu_table.item(row, 2)
        menu_id   = name_item.data(Qt.ItemDataRole.UserRole) if name_item else None

        reply = QMessageBox.question(None, "Delete Item", "Are you sure you want to delete this item?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if menu_id:
                success, message = MenuModel.delete_menu_item(menu_id)
                if success:
                    self.menu_table.removeRow(row)
                    QMessageBox.information(None, "Success", "Item deleted successfully!")
                    self.load_dashboard_stats()
                else:
                    QMessageBox.warning(None, "Error", message)
            else:
                self.menu_table.removeRow(row)

    def edit_menu_item(self, row):
        name_item = self.menu_table.item(row, 2)
        menu_id   = name_item.data(Qt.ItemDataRole.UserRole) if name_item else None

        if not menu_id:
            QMessageBox.warning(None, "Error", "Could not find item ID")
            return

        category = self.menu_table.item(row, 1).text()
        name     = self.menu_table.item(row, 2).text()
        price    = self.menu_table.item(row, 3).text().replace('₱', '').replace(',', '')
        stock    = self.menu_table.item(row, 4).text()

        dialog = EditMenuDialog(None, menu_id, category, name, price, stock, None)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            success, message = MenuModel.update_menu_item(
                menu_id, data['category'], data['name'],
                float(data['price']), data['stock'], data['image_path']
            )
            if success:
                self.load_menu_items()
                self.load_dashboard_stats()
                QMessageBox.information(None, "Success", "Item updated successfully!")
            else:
                QMessageBox.warning(None, "Error", message)

    def open_add_menu_dialog(self, parent):
        dialog = AddMenuDialog(parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not data['name'] or not data['price']:
                QMessageBox.warning(parent, "Missing Information", "Please fill in all required fields!")
                return
            try:
                price = float(data['price'].replace('₱', '').replace(',', ''))
            except ValueError:
                QMessageBox.warning(parent, "Invalid Price", "Please enter a valid price!")
                return

            success, message = MenuModel.add_menu_item(
                data['category'], data['name'], price, data['stock'], data['image_path']
            )
            if success:
                self.load_menu_items()
                self.load_dashboard_stats()
                QMessageBox.information(parent, "Success", f"Added {data['name']} to menu!")
            else:
                QMessageBox.warning(parent, "Error", message)

    # ── Data loaders ──────────────────────────────────────────────────────────

    def load_menu_items(self):
        print("📊 Loading menu items from database...")
        items = MenuModel.get_all_menu_items()
        self.menu_table.setRowCount(0)
        for item in items:
            self.add_item_to_menu_table(
                item.get('image_path'), item['category'], item['name'],
                f"₱{item['price']:.2f}", item['stock'], item['menu_id']
            )
        print(f"✅ Loaded {len(items)} menu items")

    def load_dashboard_stats(self):
        print("📊 Loading dashboard statistics...")
        stats = MenuModel.get_dashboard_stats()
        if stats:
            self.stat_cards[0].setText(str(stats['total_menu']))
            self.stat_cards[1].setText(f"₱{stats['total_revenue']:,.0f}")
            self.stat_cards[2].setText(str(stats['total_orders']))
            self.stat_cards[3].setText(str(stats['total_customers']))
            print("✅ Dashboard stats loaded")
        self.load_sales_overview()

    def load_sales_overview(self):
        print("📊 Loading sales overview...")
        sales_data = MenuModel.get_sales_overview()
        self.sales_table.setRowCount(0)
        for item in sales_data:
            row = self.sales_table.rowCount()
            self.sales_table.insertRow(row)

            name_item = QTableWidgetItem(item['name'])
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.sales_table.setItem(row, 0, name_item)

            category_item = QTableWidgetItem(item['category'])
            category_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.sales_table.setItem(row, 1, category_item)

            sales_count = item['number_of_sales'] if item['number_of_sales'] else 0
            sales_item = QTableWidgetItem(str(sales_count))
            sales_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.sales_table.setItem(row, 2, sales_item)

            revenue = item['total_revenue'] if item['total_revenue'] else 0
            revenue_item = QTableWidgetItem(f"₱{revenue:,.2f}")
            revenue_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.sales_table.setItem(row, 3, revenue_item)

        print(f"✅ Loaded {len(sales_data)} items in sales overview")

    def load_customers(self):
        print("📊 Loading customers from database...")
        customers = MenuModel.get_all_customers()
        self.customers_table.setRowCount(0)
        for customer in customers:
            row = self.customers_table.rowCount()
            self.customers_table.insertRow(row)

            def make_item(text, align=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter):
                it = QTableWidgetItem(text)
                it.setTextAlignment(align)
                it.setFlags(it.flags() & ~Qt.ItemFlag.ItemIsEditable)
                return it

            self.customers_table.setItem(row, 0, make_item(customer['username']))
            self.customers_table.setItem(row, 1, make_item(customer['email'] or 'N/A'))
            self.customers_table.setItem(row, 2, make_item(customer['phone'] or 'N/A', Qt.AlignmentFlag.AlignCenter))
            self.customers_table.setItem(row, 3, make_item(customer['address'] or 'N/A'))
            self.customers_table.setItem(row, 4, make_item(f"₱{customer['total_spent']:,.2f}", Qt.AlignmentFlag.AlignCenter))

        print(f"✅ Loaded {len(customers)} customers")

    def show_sales_report(self):
        try:
            print("🔍 Opening sales report dialog...")
            dialog = SalesReportDialog(None)
            dialog.exec()
            print("✅ Sales report dialog closed")
        except Exception as e:
            print(f"❌ Error showing sales report: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(None, "Error", f"Failed to open sales report: {str(e)}")

    def logout(self, Dialog):
        reply = QMessageBox.question(
            Dialog, "Logout", "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            print("🔒 Admin logged out")
            Dialog.close()
            from View.signINandUP import Ui_Dialog as LoginUI
            self.login_dialog = QtWidgets.QDialog()
            self.login_ui = LoginUI()
            self.login_ui.setupUi(self.login_dialog)
            self.login_dialog.show()

    def load_orders(self):
        from Model.database import Database
        print("📊 Loading orders from database...")
        connection = Database.get_connection()
        if not connection:
            return

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT
                    o.order_id,
                    u.username,
                    o.order_date,
                    o.total_amount,
                    o.status,
                    o.delivery_address,
                    GROUP_CONCAT(CONCAT(m.name, ' x', oi.quantity) SEPARATOR ', ') as items
                FROM orders o
                JOIN users u ON o.user_id = u.user_id
                JOIN order_items oi ON o.order_id = oi.order_id
                JOIN menu_items m ON oi.menu_id = m.menu_id
                GROUP BY o.order_id
                ORDER BY o.order_date DESC
            """
            cursor.execute(query)
            orders = cursor.fetchall()

            old_table = self.orders_table
            parent    = old_table.parent()
            geometry  = old_table.geometry()

            self.orders_table = QTableWidget(parent=parent)
            self.orders_table.setGeometry(geometry)
            self.orders_table.setColumnCount(5)
            self.orders_table.setHorizontalHeaderLabels(["Customer", "Date", "Items", "Total", "Status"])
            self.orders_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
            self.orders_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
            self.orders_table.setColumnWidth(0, 100)
            self.orders_table.setColumnWidth(1, 120)
            self.orders_table.setColumnWidth(2, 200)
            self.orders_table.setColumnWidth(3, 90)
            self.orders_table.setColumnWidth(4, 190)
            self.orders_table.verticalHeader().setDefaultSectionSize(50)
            self.orders_table.setStyleSheet(self.get_table_style())
            self.orders_table.setRowCount(len(orders))

            for row, order in enumerate(orders):
                customer_item = QTableWidgetItem(order['username'])
                customer_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.orders_table.setItem(row, 0, customer_item)

                date_str  = order['order_date'].strftime("%b %d, %Y") if order['order_date'] else "N/A"
                date_item = QTableWidgetItem(date_str)
                date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.orders_table.setItem(row, 1, date_item)

                self.orders_table.setItem(row, 2, QTableWidgetItem(order['items'] or 'N/A'))

                total_item = QTableWidgetItem(f"₱{order['total_amount']:,.2f}")
                total_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.orders_table.setItem(row, 3, total_item)

                status_combo = QtWidgets.QComboBox()
                status_combo.addItems(["Pending", "Processing", "Completed", "Cancelled"])
                status_combo.setCurrentText(order['status'])
                status_combo.setProperty("order_id", order['order_id'])
                status_combo.currentTextChanged.connect(
                    lambda text, combo=status_combo: self.update_order_status(
                        combo.property("order_id"), text
                    )
                )
                self.orders_table.setCellWidget(row, 4, status_combo)

            self.orders_table.show()
            print(f"✅ Loaded {len(orders)} orders")

        except Exception as e:
            print(f"❌ Error loading orders: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_order_status(self, order_id, new_status):
        from Model.database import Database
        print(f"🔄 Updating order {order_id} to status: {new_status}")
        connection = Database.get_connection()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s", (new_status, order_id))
            connection.commit()
            print(f"✅ Order {order_id} status updated to {new_status}")
            if new_status == 'Completed':
                self.load_dashboard_stats()
        except Exception as e:
            print(f"❌ Error updating order status: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()