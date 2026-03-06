import sys
from PyQt6.QtWidgets import QApplication, QDialog
from View.signINandUP import Ui_Dialog


def main():
    """Main application entry point"""
    print("🚀 Starting EatoGO Application...")

    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()

    print("✅ Application running. Login credentials:")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()