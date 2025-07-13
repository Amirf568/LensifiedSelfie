import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog, QLineEdit, QVBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from lensify.pipeline import lensify_photo 


class LensifyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lensify Sunglasses Animation")
        self.setMinimumWidth(400)

        self.input_path_edit = QLineEdit()
        self.input_path_edit.setPlaceholderText("Select input face image")

        self.output_path_edit = QLineEdit()
        self.output_path_edit.setPlaceholderText("Select output GIF file")

        self.browse_input_btn = QPushButton("Browse Input Image")
        self.browse_input_btn.clicked.connect(self.browse_input)

        self.browse_output_btn = QPushButton("Browse Output GIF")
        self.browse_output_btn.clicked.connect(self.browse_output)

        self.run_btn = QPushButton("Generate Sunglasses GIF")
        self.run_btn.clicked.connect(self.run_lensify)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Input Face Image:"))
        layout.addWidget(self.input_path_edit)
        layout.addWidget(self.browse_input_btn)
        layout.addSpacing(10)
        layout.addWidget(QLabel("Output GIF:"))
        layout.addWidget(self.output_path_edit)
        layout.addWidget(self.browse_output_btn)
        layout.addSpacing(20)
        layout.addWidget(self.run_btn)

        self.setLayout(layout)

    def browse_input(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Input Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.input_path_edit.setText(file_path)

    def browse_output(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Select Output GIF", "", "GIF Files (*.gif)"
        )
        if file_path:
            if not file_path.lower().endswith(".gif"):
                file_path += ".gif"
            self.output_path_edit.setText(file_path)

    def run_lensify(self):
        input_path = self.input_path_edit.text().strip()
        output_path = self.output_path_edit.text().strip()

        if not input_path or not Path(input_path).exists():
            QMessageBox.warning(self, "Input Error", "Please select a valid input image file.")
            return
        if not output_path:
            QMessageBox.warning(self, "Output Error", "Please select an output GIF file path.")
            return

        try:
            lensify_photo(Path(input_path), Path(output_path))
            QMessageBox.information(self, "Success", f"GIF saved to:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate GIF:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LensifyApp()
    window.show()
    sys.exit(app.exec())