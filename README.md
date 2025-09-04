# YouTube Video Downloader

A simple and user-friendly YouTube video downloader using yt-dlp with support for high-quality video downloads up to 4K. Available in both **CLI** and **GUI** versions!

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🖥️ **Dual Interface**: Choose between Command Line (CLI) or Graphical (GUI) interface
- 🎥 Download YouTube videos in various qualities (360p to 4K)
- 🎵 Audio-only downloads with format conversion
- 🔧 Automatic video+audio stream merging for high quality downloads
- 📋 Interactive format selection - see all available options and choose
- 🎨 Colored terminal output for better user experience (CLI)
- 🖱️ User-friendly graphical interface with real-time format loading (GUI)
- 🌍 Cross-platform support (Windows, macOS, Linux)
- ℹ️ Video information extraction without downloading

## 🚀 Quick Start

### Option 1: GUI (Recommended for beginners)
```bash
# Clone and setup
git clone <your-repo-url>
cd YTDownloader
pip install -r requirements.txt

# Launch GUI
python launcher.py --gui
# or simply
python gui.py
```

### Option 2: CLI (Power users)
```bash
# Clone and setup
git clone <your-repo-url>
cd YTDownloader
pip install -r requirements.txt

# Interactive mode (recommended)
python cli.py -i "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Direct download
python cli.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

## 🖥️ Interface Options

### 🎨 GUI Version (`gui.py`)
- **User-friendly graphical interface**
- **Visual format selection** - see all available qualities in a table
- **Real-time video information** display
- **Progress indicators** for downloads
- **Directory browser** for output selection
- **Perfect for beginners** and visual users

**Launch GUI:**
```bash
python gui.py
# or
python launcher.py --gui
```

### ⌨️ CLI Version (`cli.py`)
- **Command line interface** for automation and scripting
- **Interactive mode** (`-i` flag) - choose from available formats
- **Direct quality specification** for quick downloads
- **Perfect for scripts** and advanced users

**Launch CLI:**
```bash
python cli.py [options] URL
# or
python launcher.py --cli [options] URL
```

### 🔄 Universal Launcher (`launcher.py`)
Choose your preferred interface:
```bash
python launcher.py --gui    # Launch GUI
python launcher.py --cli    # Launch CLI
python launcher.py          # Default: GUI
```

## 📋 Requirements

- Python 3.7+
- yt-dlp
- colorama
- **FFmpeg** (required for high-quality video downloads that need video+audio merging)

### Installing FFmpeg

**Windows:**
- Download from: https://ffmpeg.org/download.html
- Add to your system PATH
- Or use: `winget install FFmpeg`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
sudo dnf install ffmpeg  # Fedora
sudo pacman -S ffmpeg    # Arch Linux
```

## 📦 Installation

### Option 1: Clone Repository
```bash
git clone <your-repo-url>
cd YTDownloader
pip install -r requirements.txt
```

### Option 2: Direct Download
1. Download the repository as ZIP
2. Extract to a folder
3. Open terminal in that folder
4. Run: `pip install -r requirements.txt`

## 🎯 Usage Examples

### 🖥️ GUI Usage
1. **Launch the GUI:** `python gui.py`
2. **Enter YouTube URL** in the URL field
3. **Click "Get Video Info"** to load video information
4. **Click "Load Available Formats"** to see all quality options
5. **Select your preferred format** from the table
6. **Choose output directory** (optional)
7. **Click "Download Selected Format"**

The GUI automatically shows you:
- 📺 Video information (title, duration, uploader)
- 📋 All available formats with quality, codec, and file size
- 🎵 Separate audio-only options
- ⏳ Real-time download progress

### ⌨️ CLI Usage

#### Interactive Mode (Recommended)
```bash
# Interactive format selection
python cli.py -i "https://www.youtube.com/watch?v=VIDEO_ID"
```
This will:
1. Show video information
2. List all available formats
3. Let you choose the exact format you want
4. Download your selection

#### Direct Quality Selection

**Download best quality available:**
```bash
python cli.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Download specific quality:**
```bash
python cli.py -q 1080 "https://www.youtube.com/watch?v=VIDEO_ID"
python cli.py -q 4k "https://www.youtube.com/watch?v=VIDEO_ID"
python cli.py -q 720 "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Download to specific folder:**
```bash
python cli.py -o "MyVideos" "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Audio Downloads

**Download audio only (MP3):**
```bash
python cli.py --audio-only --format mp3 "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Download audio in different formats:**
```bash
python cli.py --audio-only --format m4a "https://www.youtube.com/watch?v=VIDEO_ID"
python cli.py --audio-only --format wav "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Information & Analysis

**Get video information:**
```bash
python cli.py --info "https://www.youtube.com/watch?v=VIDEO_ID"
```

**List all available formats:**
```bash
python cli.py --list-formats "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Advanced Examples

**Download 4K video with custom output directory:**
```bash
python cli.py -q 4k -o "4K_Videos" "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Download multiple videos (using a script):**
```bash
# Create a text file with URLs (urls.txt)
# Then use a loop (example for Windows PowerShell):
Get-Content urls.txt | ForEach-Object { python cli.py $_ }
```

## 🎛️ Quality Options

| Option | Resolution | Description | Audio Included |
|--------|------------|-------------|----------------|
| `best` | Up to 4K | Best quality available (default) | ✅ Yes |
| `4k` or `2160` | 2160p | 4K Ultra HD | ✅ Yes |
| `1440` | 1440p | 2K Quad HD | ✅ Yes |
| `1080` | 1080p | Full HD | ✅ Yes |
| `720` | 720p | HD Ready | ✅ Yes |
| `480` | 480p | Standard Definition | ✅ Yes |
| `360` | 360p | Low Quality | ✅ Yes |
| `worst` | Varies | Lowest quality available | ✅ Yes |

**Note:** All video quality options automatically include audio. The app downloads the best video stream for your chosen quality and the best available audio stream, then merges them using FFmpeg. Use `--audio-only` flag if you want audio without video.

## 🔧 How High-Quality Downloads Work

Modern YouTube videos separate high-quality video and audio into different streams:

- **Low quality** (360p, some 720p): Combined video+audio streams available
- **High quality** (1080p+): Separate video-only and audio-only streams that need to be merged

This app automatically:
1. 📥 Downloads the best video-only stream for your chosen quality
2. 🎵 Downloads the best audio stream 
3. 🔗 Uses FFmpeg to merge them into a single file

**Format Selection Strategy:**
For each quality setting, the app tries multiple fallback options:
1. `bestvideo[height<=QUALITY]+bestaudio` - Best video at your quality + best audio (merged)
2. `best[height<=QUALITY]` - Best combined stream at your quality (if available)
3. Fallback to lower quality if the exact quality isn't available

This ensures you **always get audio** with your video downloads, unless you specifically use `--audio-only`.

This is why FFmpeg is required for high-quality downloads.

## 📖 Command Line Reference

```
usage: cli.py [-h] [-o OUTPUT] [-q QUALITY] [--audio-only] [--format FORMAT] 
              [--info] [--list-formats] url

positional arguments:
  url                   YouTube video URL

options:
  -h, --help            Show help message and exit
  -o, --output OUTPUT   Output directory (default: downloads)
  -q, --quality QUALITY Video quality choice:
                        {best,worst,4k,2160,1440,1080,720,480,360}
  --audio-only          Download audio only
  --format FORMAT       Output format (mp4, mp3, webm, m4a, etc.)
  --info                Show video information without downloading
  --list-formats        List all available formats for the video
```

### 🎯 Command Examples

| Command | Description |
|---------|-------------|
| `python cli.py URL` | Download best quality |
| `python cli.py -q 1080 URL` | Download 1080p quality |
| `python cli.py --audio-only URL` | Download audio only |
| `python cli.py --info URL` | Show video info |
| `python cli.py --list-formats URL` | Show available formats |
| `python cli.py -o "folder" URL` | Download to specific folder |

## 🚨 Troubleshooting

### Common Issues

#### ❌ "No FFmpeg found" error
**Solution:** Install FFmpeg and ensure it's in your system PATH.

**Verify FFmpeg installation:**
```bash
ffmpeg -version
```

#### ❌ "No formats found" error  
**Causes:** 
- Video might be private, deleted, or region-restricted
- Network connectivity issues
- Age-restricted content

**Solutions:**
- Try using `--list-formats` to see what's available
- Check if the video URL is correct and accessible
- Try a different video to test

#### ❌ Downloads are slow
**Explanation:** YouTube may throttle download speeds. This is normal behavior.

**Tips:**
- Try downloading during off-peak hours
- Consider downloading lower quality for faster speeds
- Use `--list-formats` to choose specific formats

#### ❌ Permission denied error
**Solutions:**
- Make sure you have write permissions to the output directory
- Try running with administrator privileges (Windows) or sudo (Linux/macOS)
- Choose a different output directory

#### ❌ "Why was my video low quality even with 'best' setting?"
**Explanation:** Previous versions were limited to 1080p max and only looked for combined video+audio streams. The updated version now supports up to 4K by automatically merging separate video and audio streams.

### 🔍 Debugging Tips

1. **Use `--list-formats` first** to see what's available
2. **Check the video URL** in a browser to ensure it's accessible
3. **Try with a known working video** to test your setup
4. **Check your internet connection** 
5. **Ensure FFmpeg is installed** for high-quality downloads

## 🎬 Output Information

### File Naming
Downloaded files are saved with the video title as the filename in the specified output directory (default: `downloads/`).

Example: `Rick Astley - Never Gonna Give You Up (Official Video).mp4`

### File Formats
- **Video:** MP4 (default), WebM, MKV
- **Audio:** MP3, M4A, WebM, WAV, FLAC

### Quality Information
When downloading, the app displays:
- Video title and uploader
- Video duration
- Output directory
- Selected format information

## 📚 Additional Resources

### Useful Links
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg Download](https://ffmpeg.org/download.html)
- [Python Installation](https://www.python.org/downloads/)

### Related Tools
- [youtube-dl](https://github.com/ytdl-org/youtube-dl) - Original YouTube downloader
- [4K Video Downloader](https://www.4kdownload.com/) - GUI alternative
- [JDownloader](https://jdownloader.org/) - Multi-platform download manager

## ⚖️ Legal Notice

**Important:** This tool is for educational and personal use only. 

- Respect YouTube's Terms of Service
- Respect copyright laws and intellectual property rights
- Only download videos you have permission to download
- Consider videos in the public domain or Creative Commons licensed content
- Do not redistribute copyrighted content

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Made with ❤️ for the YouTube downloading community**
