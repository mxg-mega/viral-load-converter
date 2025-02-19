import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, 
    QDialog, QFormLayout, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor
from models.hbvl_model import HBVLModel
from models.hcvl_model import HCVLModel
from models.hivl_model import HIVLModel
from config import Config

class StyledFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            StyledFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
        """)

class SettingsDialog(QDialog):
    def __init__(self, hbvl_model, hcvl_model, hivl_model, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                font-weight: bold;
            }
        """)

        self.hbvl_model = hbvl_model
        self.hcvl_model = hcvl_model
        self.hivl_model = hivl_model

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Create a frame for the settings
        settings_frame = StyledFrame()
        settings_layout = QFormLayout()

        # Input fields with better styling
        self.hbvl_constant_input = QLineEdit(str(self.hbvl_model.conversion_constant))
        self.hcvl_constant_input = QLineEdit(str(self.hcvl_model.conversion_constant))
        self.hivl_constant_input = QLineEdit(str(self.hivl_model.conversion_constant))

        settings_layout.addRow("HBVL Constant:", self.hbvl_constant_input)
        settings_layout.addRow("HCVL Constant:", self.hcvl_constant_input)
        settings_layout.addRow("HIVL Constant:", self.hivl_constant_input)
        settings_frame.setLayout(settings_layout)
        
        layout.addWidget(settings_frame)

        # Buttons in horizontal layout
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            background-color: #6c757d;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            min-width: 100px;
        """)
        
        save_button.clicked.connect(self.save_constants)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_constants(self):
        try:
            constants = {
                'HBVL': float(self.hbvl_constant_input.text()),
                'HCVL': float(self.hcvl_constant_input.text()),
                'HIVL': float(self.hivl_constant_input.text())
            }
            
            for name, value in constants.items():
                if value <= 0:
                    raise ValueError(f"{name} constant must be greater than 0")
                Config.set_constant(f"{name}_CONSTANT", value)

            QMessageBox.information(self, "Success", "Constants updated successfully!")
            self.accept()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

class ResultsWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            ResultsWidget {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
            QLabel {
                color: #212529;
                font-size: 14px;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.iu_label = QLabel("IU/ml: -")
        self.log_label = QLabel("Log10: -")
        
        self.layout.addWidget(self.iu_label)
        self.layout.addWidget(self.log_label)

    def update_results(self, iu_per_ml, log_value):
        self.iu_label.setText(f"IU/ml: {iu_per_ml:.5f}")
        self.log_label.setText(f"Log10: {log_value:.5f}")

class ViralLoadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Viral Load Calculator")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
                min-width: 200px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                color: #212529;
                font-weight: bold;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Input section
        input_frame = StyledFrame()
        input_layout = QVBoxLayout()

        # Viral load type selection
        type_layout = QHBoxLayout()
        type_label = QLabel("Select Viral Load Type:")
        self.viral_load_type = QComboBox()
        self.viral_load_type.addItems(["HBVL", "HCVL", "HIVL"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.viral_load_type)
        input_layout.addLayout(type_layout)

        # Result input
        result_layout = QHBoxLayout()
        result_label = QLabel("Input Result:")
        self.result_input = QLineEdit()
        self.result_input.setPlaceholderText("Enter result value")
        result_layout.addWidget(result_label)
        result_layout.addWidget(self.result_input)
        input_layout.addLayout(result_layout)

        input_frame.setLayout(input_layout)
        layout.addWidget(input_frame)

        # Buttons
        button_layout = QHBoxLayout()
        self.calculate_button = QPushButton("Calculate")
        self.settings_button = QPushButton("Settings")
        self.settings_button.setStyleSheet("""
            background-color: #6c757d;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            min-width: 100px;
        """)
        
        self.calculate_button.clicked.connect(self.calculate)
        self.settings_button.clicked.connect(self.open_settings)
        
        button_layout.addWidget(self.settings_button)
        button_layout.addWidget(self.calculate_button)
        layout.addLayout(button_layout)

        # Results section
        self.results_widget = ResultsWidget()
        layout.addWidget(self.results_widget)

        # Set layout
        central_widget.setLayout(layout)

        # Initialize models
        self.hbvl_model = HBVLModel(0)
        self.hcvl_model = HCVLModel(0)
        self.hivl_model = HIVLModel(0)

    def calculate(self):
        try:
            selected_type = self.viral_load_type.currentText()
            result_text = self.result_input.text().strip()
            
            if not result_text:
                raise ValueError("Result cannot be empty")
            
            result = float(result_text)
            if result <= 0:
                raise ValueError("Result must be greater than 0")

            model_map = {
                "HBVL": self.hbvl_model,
                "HCVL": self.hcvl_model,
                "HIVL": self.hivl_model
            }
            
            model = model_map.get(selected_type)
            if not model:
                raise ValueError("Invalid viral load type")
                
            model.result = result
            iu_per_ml = model.convert_to_IU_per_ml()
            log_value = model.get_value_log()

            self.results_widget.update_results(iu_per_ml, log_value)

        except (ValueError, TypeError) as e:
            QMessageBox.critical(self, "Error", str(e))

    def open_settings(self):
        settings_dialog = SettingsDialog(
            self.hbvl_model, 
            self.hcvl_model, 
            self.hivl_model, 
            self
        )
        settings_dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ViralLoadApp()
    window.show()
    sys.exit(app.exec())