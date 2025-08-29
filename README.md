# YouTube Video Downloader

A simple and user-friendly YouTube video downloader using yt-dlp with support for high-quality video downloads up to 4K.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🎥 Download YouTube videos in various qualities (360p to 4K)
- 🎵 Audio-only downloads with format conversion
- 🔧 Automatic video+audio stream merging for high quality downloads
- 📋 List available formats for any video
- 🎨 Colored terminal output for better user experience
- 🌍 Cross-platform support (Windows, macOS, Linux)
- ℹ️ Video information extraction without downloading

## 🚀 Quick Start

1. **Install Python 3.7+** if you haven't already
2. **Clone this repository:**
   ```bash
   git clone <your-repo-url>
   cd YTDownloader
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Download a video:**
   ```bash
   python app.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
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

### Basic Downloads

**Download best quality available:**
```bash
python app.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Download specific quality:**
```bash
python app.py -q 1080 "https://www.youtube.com/watch?v=VIDEO_ID"
python app.py -q 4k "https://www.youtube.com/watch?v=VIDEO_ID"
python app.py -q 720 "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Download to specific folder:**
```bash
python app.py -o "MyVideos" "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Audio Downloads

**Download audio only (MP3):**
```bash
python app.py --audio-only --format mp3 "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Download audio in different formats:**
```bash
python app.py --audio-only --format m4a "https://www.youtube.com/watch?v=VIDEO_ID"
python app.py --audio-only --format wav "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Information & Analysis

**Get video information:**
```bash
python app.py --info "https://www.youtube.com/watch?v=VIDEO_ID"
```

**List all available formats:**
```bash
python app.py --list-formats "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Advanced Examples

**Download 4K video with custom output directory:**
```bash
python app.py -q 4k -o "4K_Videos" "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Download multiple videos (using a script):**
```bash
# Create a text file with URLs (urls.txt)
# Then use a loop (example for Windows PowerShell):
Get-Content urls.txt | ForEach-Object { python app.py $_ }
```

## 🎛️ Quality Options

| Option | Resolution | Description |
|--------|------------|-------------|
| `best` | Up to 4K | Best quality available (default) |
| `4k` or `2160` | 2160p | 4K Ultra HD |
| `1440` | 1440p | 2K Quad HD |
| `1080` | 1080p | Full HD |
| `720` | 720p | HD Ready |
| `480` | 480p | Standard Definition |
| `360` | 360p | Low Quality |
| `worst` | Varies | Lowest quality available |

## 🔧 How High-Quality Downloads Work

Modern YouTube videos separate high-quality video and audio into different streams:

- **Low quality** (360p, some 720p): Combined video+audio streams available
- **High quality** (1080p+): Separate video-only and audio-only streams that need to be merged

This app automatically:
1. 📥 Downloads the best video-only stream for your chosen quality
2. 🎵 Downloads the best audio stream 
3. 🔗 Uses FFmpeg to merge them into a single file

This is why FFmpeg is required for high-quality downloads.

## 📖 Command Line Reference

```
usage: app.py [-h] [-o OUTPUT] [-q QUALITY] [--audio-only] [--format FORMAT] 
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
| `python app.py URL` | Download best quality |
| `python app.py -q 1080 URL` | Download 1080p quality |
| `python app.py --audio-only URL` | Download audio only |
| `python app.py --info URL` | Show video info |
| `python app.py --list-formats URL` | Show available formats |
| `python app.py -o "folder" URL` | Download to specific folder |

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
