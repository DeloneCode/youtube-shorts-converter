import sys
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QLabel, QFileDialog, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip
import tempfile

class VideoConverterThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, input_path, output_path):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        try:
            # Load the video
            video = VideoFileClip(self.input_path)
            
            # Calculate new dimensions for 9:16 aspect ratio
            target_height = 1920
            target_width = 1080
            
            # Calculate scaling factor
            scale = min(target_width / video.w, target_height / video.h)
            new_width = int(video.w * scale)
            new_height = int(video.h * scale)
            
            # Create black background
            background = ColorClip(size=(target_width, target_height), color=(0, 0, 0))
            background = background.set_duration(video.duration)
            
            # Create a function to resize frames using OpenCV
            def resize_frame(frame):
                return cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
            
            # Apply the resize function to the video
            resized_video = video.fl_image(resize_frame)
            
            # Center the video on black background
            x_offset = (target_width - new_width) // 2
            y_offset = (target_height - new_height) // 2
            
            # Position the resized video
            resized_video = resized_video.set_position((x_offset, y_offset))
            
            # Composite the videos
            final_video = CompositeVideoClip([background, resized_video])
            
            # Write the output file
            final_video.write_videofile(
                self.output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=tempfile.gettempdir() + '/temp-audio.m4a',
                remove_temp=True
            )
            
            # Clean up
            video.close()
            background.close()
            resized_video.close()
            final_video.close()
            
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(str(e))

class VideoConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Shorts Video Converter")
        self.setMinimumSize(600, 400)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create and style widgets
        self.title_label = QLabel("YouTube Shorts Video Converter")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        
        self.select_button = QPushButton("Select Video")
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 5px;
                font-size: 16px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.file_label = QLabel("No file selected")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setStyleSheet("font-size: 14px; color: #666;")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        self.progress_bar.hide()
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px;")
        
        # Add widgets to layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        
        # Connect signals
        self.select_button.clicked.connect(self.select_file)
        
        self.input_file = None
        self.converter_thread = None

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*.*)"
        )
        
        if file_name:
            self.input_file = file_name
            self.file_label.setText(f"Selected: {os.path.basename(file_name)}")
            self.convert_video()

    def convert_video(self):
        if not self.input_file:
            return
            
        output_file, _ = QFileDialog.getSaveFileName(
            self,
            "Save Converted Video",
            os.path.splitext(self.input_file)[0] + "_shorts.mp4",
            "MP4 Files (*.mp4)"
        )
        
        if output_file:
            self.progress_bar.show()
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            self.status_label.setText("Converting video...")
            self.select_button.setEnabled(False)
            
            self.converter_thread = VideoConverterThread(self.input_file, output_file)
            self.converter_thread.finished.connect(self.conversion_finished)
            self.converter_thread.error.connect(self.conversion_error)
            self.converter_thread.start()

    def conversion_finished(self):
        self.progress_bar.hide()
        self.status_label.setText("Conversion completed successfully!")
        self.select_button.setEnabled(True)

    def conversion_error(self, error_message):
        self.progress_bar.hide()
        self.status_label.setText(f"Error: {error_message}")
        self.select_button.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    window = VideoConverterApp()
    window.show()
    sys.exit(app.exec_()) 