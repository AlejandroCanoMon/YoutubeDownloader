# 🎬 YouTubeDownloader 

A lightweight GUI tool built with Python and `yt-dlp` to download YouTube videos in your preferred resolution. Combines video and audio streams using FFmpeg.

## 📦 Features

- Easy-to-use graphical interface with `tkinter`
- Select desired video resolution before downloading
- Automatically merges video + audio using `FFmpeg`
- Fully compatible with the latest YouTube layouts
- No need for browser extensions or ads

---

## 🗂️ Project Structure

To work correctly, your project folder **must include FFmpeg** with the following structure:
```\
📁 YoutubeDownloader/
├── ffmpeg/
│   └── bin/
│       └── ffmpeg.exe
├── youtube.py

```

- `ffmpeg/bin/ffmpeg.exe` → This is the binary needed to merge video + audio.
- `downloader.py` → Python script.

If you package the project as a `.exe` with PyInstaller, make sure the FFmpeg folder is placed **next to the executable**, like so:


```
📁 YouTubeDownloader/
├── ffmpeg/
│   └── bin/
│       └── ffmpeg.exe
├── youtube.exe

```

---

## 🔗 Download FFmpeg

To get FFmpeg, download the **latest static build** from the official repository:

📥 [Download FFmpeg (Win64 static)](https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-win64-gpl.zip)

After downloading:
1. Extract the `.zip` file.
2. Rename the extracted folder to `ffmpeg`.
3. Place the folder next to your `.py` or `.exe` file, as shown above.

---

## 🚀 How to Run

If you're using the `.py` version:
```
\bash
python youtube.py
\
```

If you're using the `.exe` version (from PyInstaller), just double-click `youtube.exe`.

---

## 📦 Building a Portable Executable (Optional)

If you want to package the project into a `.exe` file:

1. Install PyInstaller:
\```bash
pip install pyinstaller
\```

2. Generate the executable:
\```bash
pyinstaller --onefile youtube.py
\```

3. Move the `ffmpeg` folder next to the `.exe` in the `dist/` directory.

---

## 🧠 Requirements

- Python 3.9+
- `yt-dlp`
- `tkinter` (standard in most Python installations)

Install dependencies with:

\```bash
pip install yt-dlp
\```

---

## 🛠️ Credits

Built by [Alex](https://github.com/AlejandroCanoMon) — Software Engineer & Cybersecurity Specialist.

---

## 📃 License

MIT License. Free to use and modify.
