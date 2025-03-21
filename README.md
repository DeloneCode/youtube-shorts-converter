[![youtube-converter.png](https://i.postimg.cc/3RD1ThXn/youtube-converter.png)](https://postimg.cc/Q9h1QRnT)
# YouTube Shorts Video Converter

A Python application that converts videos to YouTube Shorts format (9:16 aspect ratio) with a modern PyQt5 GUI.

## Features

- Convert videos to YouTube Shorts format (1080x1920)
- Maintains aspect ratio while adding black bars
- Modern and user-friendly interface
- Progress tracking
- Supports multiple video formats (MP4, AVI, MOV, MKV)

## Requirements

- Python 3.12 or higher
- PyQt5
- moviepy
- numpy
- opencv-python

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-shorts-converter.git
cd youtube-shorts-converter
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python video_converter.py
```

2. Click "Select Video" to choose your input video file
3. Choose the output location for the converted video
4. Wait for the conversion to complete

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## How it Works

The application:
1. Takes any video input
2. Resizes it to fit within 1080x1920 pixels while maintaining aspect ratio
3. Adds black bars where necessary to achieve the 9:16 aspect ratio
4. Centers the video content
5. Saves the result in MP4 format

## Notes

- The conversion process may take some time depending on the video size and your computer's specifications
- The output video will be saved with "_shorts" appended to the original filename
- Make sure you have enough disk space for the conversion process 
