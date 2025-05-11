# 🎬 YouTubeDownloader

A lightweight GUI built with Python and `yt-dlp` to download YouTube videos with your chosen resolution, merging video and audio using FFmpeg.

---

## ⚙️ Requirements

- Python 3.9+
- `yt-dlp`
- `tkinter` (usually included with Python)
- FFmpeg (either installed or placed in project folder)

Install required Python packages:

`pip install -r requirements.txt`

---

## 🗂️ Folder Structure

Place FFmpeg as follows if using the portable version:

📁 YoutubeDownloader/
├── ffmpeg/
│   └── bin/
│       └── ffmpeg.exe
├── youtube.py

If FFmpeg is added to your system PATH, the portable folder is not necessary.

---

## 🚀 Running the App

Run the script with:

`python youtube.py`

---

## 🧰 Optional: Build an Executable

To create a `.exe` (requires FFmpeg next to the binary):

1. Install PyInstaller:

`pip install pyinstaller`

2. Build the executable:

`pyinstaller --onefile youtube.py`

3. Place the `ffmpeg` folder (same structure) next to `youtube.exe` inside `/dist`.

---

## 📥 Download FFmpeg

Download the latest static Win64 build:

https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-win64-gpl.zip

Extract it, rename the folder to `ffmpeg`, and ensure `ffmpeg.exe` is inside `ffmpeg/bin/`.

---

## 📃 License

MIT License.
