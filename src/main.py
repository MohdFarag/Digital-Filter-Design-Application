import sys
from PyQt5.QtWidgets import QApplication
from app import MainWindow

try:
    from qdarktheme import load_stylesheet
except:
    def load_stylesheet(style):
        return ""

def main():
    """Main function for the application."""
    # Create the application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(load_stylesheet("light"))

    # Create and show the main window
    window = MainWindow()
    window.show()

    print("Application started successfully.")
    # Start the event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
