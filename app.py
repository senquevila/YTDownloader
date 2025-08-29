#!/usr/bin/env python3
"""
YouTube Video Downloader
A simple and user-friendly YouTube video downloader using yt-dlp
"""

import os
import sys
import argparse
from pathlib import Path
import yt_dlp
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class YouTubeDownloader:
    def __init__(self, output_dir="downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def download_video(self, url, quality="best", audio_only=False, output_format=None):
        """
        Download a YouTube video

        Args:
            url (str): YouTube video URL
            quality (str): Video quality preference
            audio_only (bool): Download audio only
            output_format (str): Output format (mp4, mp3, etc.)
        """
        try:
            # Configure yt-dlp options
            ydl_opts = {
                "outtmpl": str(self.output_dir / "%(title)s.%(ext)s"),
                "noplaylist": True,
                # Ensure ffmpeg is used for merging when needed
                "merge_output_format": "mp4",
            }

            if audio_only:
                ydl_opts.update(
                    {
                        "format": "bestaudio/best",
                        "postprocessors": [
                            {
                                "key": "FFmpegExtractAudio",
                                "preferredcodec": output_format or "mp3",
                                "preferredquality": "192",
                            }
                        ],
                    }
                )
            else:
                # Configure video format selection
                if quality == "best":
                    # Try to get the best quality available, merging video and audio if needed
                    ydl_opts["format"] = "bestvideo[height<=2160]+bestaudio/best[height<=2160]/bestvideo+bestaudio/best"
                elif quality == "worst":
                    ydl_opts["format"] = "worst"
                elif quality == "4k" or quality == "2160":
                    ydl_opts["format"] = "bestvideo[height<=2160]+bestaudio/best[height<=2160]"
                elif quality == "1440":
                    ydl_opts["format"] = "bestvideo[height<=1440]+bestaudio/best[height<=1440]"
                elif quality == "1080":
                    ydl_opts["format"] = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
                elif quality == "720":
                    ydl_opts["format"] = "bestvideo[height<=720]+bestaudio/best[height<=720]"
                elif quality == "480":
                    ydl_opts["format"] = "bestvideo[height<=480]+bestaudio/best[height<=480]"
                elif quality == "360":
                    ydl_opts["format"] = "bestvideo[height<=360]+bestaudio/best[height<=360]"
                else:
                    # For custom quality, try to get the requested resolution
                    ydl_opts["format"] = f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]"

                if output_format:
                    ydl_opts["postprocessors"] = [
                        {
                            "key": "FFmpegVideoConvertor",
                            "preferedformat": output_format,
                        }
                    ]

            print(f"{Fore.CYAN}Starting download...{Style.RESET_ALL}")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                info = ydl.extract_info(url, download=False)
                title = info.get("title", "Unknown")
                duration = info.get("duration", 0)
                uploader = info.get("uploader", "Unknown")

                print(f"{Fore.GREEN}Title:{Style.RESET_ALL} {title}")
                print(f"{Fore.GREEN}Uploader:{Style.RESET_ALL} {uploader}")
                print(
                    f"{Fore.GREEN}Duration:{Style.RESET_ALL} {duration // 60}:{duration % 60:02d}"
                )
                print(
                    f"{Fore.GREEN}Output Directory:{Style.RESET_ALL} {self.output_dir.absolute()}"
                )

                # Download the video
                ydl.download([url])

            print(f"{Fore.GREEN}✓ Download completed successfully!{Style.RESET_ALL}")

        except yt_dlp.DownloadError as e:
            print(f"{Fore.RED}Download Error: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Unexpected Error: {e}{Style.RESET_ALL}")

    def list_available_formats(self, url):
        """List all available formats for a YouTube video"""
        try:
            ydl_opts = {"quiet": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                print(f"{Fore.CYAN}Available formats for: {info.get('title', 'Unknown')}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
                
                formats = info.get('formats', [])
                
                # Group formats
                video_formats = []
                audio_formats = []
                
                for f in formats:
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        video_formats.append((f, 'video+audio'))
                    elif f.get('vcodec') != 'none':
                        video_formats.append((f, 'video-only'))
                    elif f.get('acodec') != 'none':
                        audio_formats.append((f, 'audio-only'))
                
                # Sort by quality
                video_formats.sort(key=lambda x: x[0].get('height', 0) if x[0].get('height') else 0, reverse=True)
                
                print(f"{Fore.GREEN}VIDEO FORMATS:{Style.RESET_ALL}")
                for f, ftype in video_formats[:15]:  # Show top 15
                    height = f.get('height', 'unknown')
                    ext = f.get('ext', 'unknown')
                    fps = f" {f.get('fps')}fps" if f.get('fps') else ""
                    vcodec = f.get('vcodec', 'unknown')
                    size = f" ({f.get('filesize', 0) // 1024 // 1024}MB)" if f.get('filesize') else ""
                    print(f"  {f.get('format_id')}: {height}p {ext} {vcodec}{fps} [{ftype}]{size}")
                
                print(f"\n{Fore.GREEN}AUDIO FORMATS:{Style.RESET_ALL}")
                for f, ftype in audio_formats[:5]:  # Show top 5
                    ext = f.get('ext', 'unknown')
                    acodec = f.get('acodec', 'unknown')
                    abr = f" {f.get('abr')}kbps" if f.get('abr') else ""
                    size = f" ({f.get('filesize', 0) // 1024 // 1024}MB)" if f.get('filesize') else ""
                    print(f"  {f.get('format_id')}: {ext} {acodec}{abr}{size}")
                    
        except Exception as e:
            print(f"{Fore.RED}Error listing formats: {e}{Style.RESET_ALL}")

    def get_video_info(self, url):
        """Get information about a YouTube video without downloading"""
        try:
            ydl_opts = {"quiet": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                print(f"{Fore.CYAN}Video Information:{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Title:{Style.RESET_ALL} {info.get('title', 'N/A')}")
                print(
                    f"{Fore.GREEN}Uploader:{Style.RESET_ALL} {info.get('uploader', 'N/A')}"
                )
                print(
                    f"{Fore.GREEN}Duration:{Style.RESET_ALL} {info.get('duration', 0) // 60}:{info.get('duration', 0) % 60:02d}"
                )
                print(
                    f"{Fore.GREEN}View Count:{Style.RESET_ALL} {info.get('view_count', 'N/A'):,}"
                )
                print(
                    f"{Fore.GREEN}Upload Date:{Style.RESET_ALL} {info.get('upload_date', 'N/A')}"
                )
                print(
                    f"{Fore.GREEN}Description:{Style.RESET_ALL} {info.get('description', 'N/A')[:200]}..."
                )

        except Exception as e:
            print(f"{Fore.RED}Error getting video info: {e}{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos using yt-dlp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python app.py "https://www.youtube.com/watch?v=VIDEO_ID"
  python app.py -q 1080 -o downloads "https://www.youtube.com/watch?v=VIDEO_ID"
  python app.py -q 4k "https://www.youtube.com/watch?v=VIDEO_ID"
  python app.py --audio-only --format mp3 "https://www.youtube.com/watch?v=VIDEO_ID"
  python app.py --info "https://www.youtube.com/watch?v=VIDEO_ID"
  python app.py --list-formats "https://www.youtube.com/watch?v=VIDEO_ID"

Note: For high quality videos (1080p+), FFmpeg is required to merge video and audio streams.
        """,
    )

    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "-o",
        "--output",
        default="downloads",
        help="Output directory (default: downloads)",
    )
    parser.add_argument(
        "-q",
        "--quality",
        default="best",
        choices=["best", "worst", "4k", "2160", "1440", "1080", "720", "480", "360"],
        help="Video quality (default: best, supports: 4k/2160p, 1440p, 1080p, 720p, 480p, 360p)",
    )
    parser.add_argument("--audio-only", action="store_true", help="Download audio only")
    parser.add_argument("--format", help="Output format (mp4, mp3, etc.)")
    parser.add_argument(
        "--info", action="store_true", help="Show video information without downloading"
    )
    parser.add_argument(
        "--list-formats", action="store_true", help="List all available formats for the video"
    )

    args = parser.parse_args()

    # Validate URL
    if not ("youtube.com" in args.url or "youtu.be" in args.url):
        print(f"{Fore.RED}Error: Please provide a valid YouTube URL{Style.RESET_ALL}")
        sys.exit(1)

    downloader = YouTubeDownloader(args.output)

    if args.info:
        downloader.get_video_info(args.url)
    elif args.list_formats:
        downloader.list_available_formats(args.url)
    else:
        downloader.download_video(
            args.url,
            quality=args.quality,
            audio_only=args.audio_only,
            output_format=args.format,
        )


if __name__ == "__main__":
    print(f"{Fore.MAGENTA}🎥 YouTube Video Downloader{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'=' * 30}{Style.RESET_ALL}")
    main()
