import sys
import json
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton
from config import load_config, save_config  # Import config handling functions

CONFIG_FILE = "config.json"

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        # Load existing settings
        self.config = load_config()

        # Form layout for settings
        form_layout = QFormLayout()

        self.video_path_input = QLineEdit(self.config.get("video_save_path", "videos/"))
        self.api_key_input = QLineEdit(self.config.get("youtube_api_key", ""))
        
        form_layout.addRow(QLabel("Video Save Path:"), self.video_path_input)
        form_layout.addRow(QLabel("YouTube API Key:"), self.api_key_input)

        layout.addLayout(form_layout)

        # Save button
        self.save_button = QPushButton("Save & Close")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_settings(self):
        self.config["video_save_path"] = self.video_path_input.text()
        self.config["youtube_api_key"] = self.api_key_input.text()

        save_config(self.config)  # Save to file
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())
