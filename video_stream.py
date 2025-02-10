import cv2
import threading
import os
from datetime import datetime
from config import load_config

class VideoStream:
    def __init__(self, device_index=0):
        self.device_index = device_index  # Default V4L2 device
        self.cap = None
        self.recording = False
        self.video_writer = None
        self.output_path = None
        self.fps = 30  # Set a default FPS

    def start_capture(self):
        """Starts video capture and recording."""
        self.cap = cv2.VideoCapture(self.device_index)
        if not self.cap.isOpened():
            print("Error: Unable to open video device.")
            return

        # Load config for save path
        config = load_config()
        save_directory = config.get("video_save_path", "videos/")
        os.makedirs(save_directory, exist_ok=True)

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_path = os.path.join(save_directory, f"recording_{timestamp}.mp4")

        # Ensure valid FPS
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0 or fps is None:
            fps = self.fps  # Use default if invalid

        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_size = (frame_width, frame_height)

        # Video writer settings
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(self.output_path, fourcc, fps, frame_size)

        self.recording = True
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()

    def _capture_loop(self):
        """Background thread for video recording."""
        while self.recording and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break  # Stop if no frame is read

            self.video_writer.write(frame)  # Save frame

        self.stop_capture()

    def stop_capture(self):
        """Stops video capture and closes resources."""
        if not self.recording:
            return
        
        self.recording = False
        if self.cap:
            self.cap.release()
            self.cap = None
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        print(f"Video saved to: {self.output_path}")

    def is_recording(self):
        return self.recording
