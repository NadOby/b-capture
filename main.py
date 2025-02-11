import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMenuBar, QMenu
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
from video_stream import VideoStream  # Import VideoStream

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("V4L Video Recorder")
        self.setGeometry(100, 100, 800, 600)

        # Layout
        layout = QVBoxLayout()

        # Video Display (Now connected to VideoStream)
        self.video_label = QLabel("Video Stream Placeholder", self)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("background-color: black; color: white; font-size: 16px;")
        layout.addWidget(self.video_label)

        # Control Buttons
        self.start_button = QPushButton("Start Recording")
        self.stop_button = QPushButton("Stop Recording")
        self.zoom_button = QPushButton("Zoom (Stub)")
        self.focus_button = QPushButton("Focus (Stub)")
        self.upload_button = QPushButton("Upload to YouTube (Stub)")

        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.zoom_button)
        layout.addWidget(self.focus_button)
        layout.addWidget(self.upload_button)

        # Menu Bar
        self.menu_bar = QMenuBar(self)
        settings_menu = QMenu("Settings", self)
        settings_menu.addAction("Open Settings", self.open_settings)
        self.menu_bar.addMenu(settings_menu)

        layout.setMenuBar(self.menu_bar)
        self.setLayout(layout)

        # Initialize Video Stream
        self.video_stream = VideoStream()
        self.video_stream.new_frame_signal.connect(self.update_video)

        # Connect buttons to actions
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

    def update_video(self, frame: QImage):
        """Update QLabel with new video frame."""
        pixmap = QPixmap.fromImage(frame)
        self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def start_recording(self):
        if not self.video_stream.is_recording():
            self.video_stream.start_capture()
            print("Recording started.")

    def stop_recording(self):
        if self.video_stream.is_recording():
            self.video_stream.stop_capture()
            print("Recording stopped.")

    def open_settings(self):
        print("Settings window would open here (to be implemented).")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
