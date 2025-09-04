#!/usr/bin/env python3
"""
YouTube Video Downloader (CLI)
A simple and user-friendly YouTube video downloader using yt-dlp
"""

import argparse
import sys

from colorama import Fore, Style, init

from downloader_service import YouTubeDownloaderService

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class YouTubeDownloaderCLI:
    def __init__(self, output_dir="downloads"):
        self.service = YouTubeDownloaderService(output_dir)

    def download_video(
        self,
        url,
        quality="best",
        audio_only=False,
        output_format=None,
        interactive=False,
    ):
        """
        Download a YouTube video using the centralized service
        """
        try:
            # If interactive mode, let user choose the format
            if interactive:
                selected_format = self.interactive_format_selection(url)
                if not selected_format:
                    print(f"{Fore.YELLOW}Download cancelled by user.{Style.RESET_ALL}")
                    return
                # Use the selected format
                quality = selected_format["quality"]
                audio_only = selected_format["audio_only"]
                output_format = selected_format.get("output_format")

            # Preview what will be downloaded
            preview = self.service.preview_download(url, quality, audio_only)

            print(f"{Fore.CYAN}Download Preview:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Title:{Style.RESET_ALL} {preview['title']}")
            print(f"{Fore.GREEN}Uploader:{Style.RESET_ALL} {preview['uploader']}")
            duration = preview["duration"]
            print(
                f"{Fore.GREEN}Duration:{Style.RESET_ALL} {duration // 60}:{duration % 60:02d}"
            )
            print(f"{Fore.GREEN}Quality:{Style.RESET_ALL} {quality}")
            print(
                f"{Fore.GREEN}Mode:{Style.RESET_ALL} {'Audio Only' if audio_only else 'Video + Audio'}"
            )
            print(
                f"{Fore.GREEN}Output Directory:{Style.RESET_ALL} {preview['output_dir']}"
            )
            print()

            # Ask user for confirmation
            response = input(
                f"{Fore.YELLOW}Do you want to proceed with the download? (y/n): {Style.RESET_ALL}"
            )
            if response.lower() not in ["y", "yes"]:
                print(f"{Fore.YELLOW}Download cancelled by user.{Style.RESET_ALL}")
                return

            print(f"{Fore.CYAN}Starting download...{Style.RESET_ALL}")

            # Progress callback for CLI
            def progress_hook(d):
                if d["status"] == "downloading":
                    try:
                        percent = d.get("_percent_str", "N/A")
                        speed = d.get("_speed_str", "N/A")
                        print(
                            f"\r{Fore.CYAN}Downloading... {percent} at {speed}{Style.RESET_ALL}",
                            end="",
                            flush=True,
                        )
                    except:
                        print(
                            f"\r{Fore.CYAN}Downloading...{Style.RESET_ALL}",
                            end="",
                            flush=True,
                        )
                elif d["status"] == "finished":
                    print(
                        f"\n{Fore.GREEN}Download finished: {d['filename']}{Style.RESET_ALL}"
                    )

            # Download using the service
            result = self.service.download_video(
                url=url,
                quality=quality,
                audio_only=audio_only,
                output_format=output_format,
                progress_callback=progress_hook,
            )

            print(f"{Fore.GREEN}✓ {result['message']}{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def interactive_format_selection(self, url):
        """Allow user to interactively select video format using the service"""
        try:
            # Get video info
            info = self.service.get_video_info(url)

            print(f"{Fore.CYAN}Video: {info['title']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Uploader: {info['uploader']}{Style.RESET_ALL}")
            duration = info["duration"]
            print(
                f"{Fore.CYAN}Duration: {duration // 60}:{duration % 60:02d}{Style.RESET_ALL}"
            )
            print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")

            # Get format options
            options = self.service.get_format_selection_options(url)

            print(f"{Fore.GREEN}📹 VIDEO OPTIONS:{Style.RESET_ALL}")
            video_options = [opt for opt in options if opt["type"] == "video"]
            for opt in video_options:
                print(
                    f"  {Fore.YELLOW}{opt['num']:2d}.{Style.RESET_ALL} {opt['description']}"
                )

            print(f"\n{Fore.GREEN}🎵 AUDIO OPTIONS:{Style.RESET_ALL}")
            audio_options = [opt for opt in options if opt["type"] == "audio"]
            for opt in audio_options:
                print(
                    f"  {Fore.YELLOW}{opt['num']:2d}.{Style.RESET_ALL} {opt['description']}"
                )

            cancel_num = len(options) + 1
            print(f"\n{Fore.YELLOW}{cancel_num:2d}.{Style.RESET_ALL} Cancel download")

            # Get user selection
            while True:
                try:
                    print()
                    choice = input(
                        f"{Fore.CYAN}Select an option (1-{cancel_num}): {Style.RESET_ALL}"
                    )
                    choice_num = int(choice)

                    if choice_num == cancel_num:  # Cancel option
                        return None
                    elif 1 <= choice_num <= len(options):
                        selected = next(
                            (opt for opt in options if opt["num"] == choice_num), None
                        )
                        if selected:
                            print(
                                f"{Fore.GREEN}✓ Selected: {selected['description']}{Style.RESET_ALL}"
                            )
                            return selected
                    else:
                        print(
                            f"{Fore.RED}Invalid option. Please choose between 1 and {cancel_num}.{Style.RESET_ALL}"
                        )
                except ValueError:
                    print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
                except KeyboardInterrupt:
                    print(
                        f"\n{Fore.YELLOW}Download cancelled by user.{Style.RESET_ALL}"
                    )
                    return None

        except Exception as e:
            print(f"{Fore.RED}Error during format selection: {e}{Style.RESET_ALL}")
            return None

    def list_available_formats(self, url, selected_quality=None, audio_only=False):
        """List all available formats for a YouTube video using the service"""
        try:
            formats = self.service.get_available_formats(url)
            info = self.service.get_video_info(url)

            print(f"{Fore.CYAN}Available formats for: {info['title']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

            # Show what will be downloaded based on current settings
            if audio_only:
                print(f"{Fore.YELLOW}Mode: Audio Only{Style.RESET_ALL}")
            else:
                print(
                    f"{Fore.YELLOW}Selected Quality: {selected_quality or 'best'}{Style.RESET_ALL}"
                )
            print()

            # Group formats
            video_formats = [
                f for f in formats if f["type"] in ["Video+Audio", "Video Only"]
            ]
            audio_formats = [f for f in formats if f["type"] == "Audio Only"]

            if not audio_only and video_formats:
                print(f"{Fore.GREEN}VIDEO FORMATS:{Style.RESET_ALL}")
                for f in video_formats[:15]:  # Show top 15
                    height = f["height"] or "unknown"
                    ext = f["ext"]
                    fps = f" {f['fps']}fps" if f["fps"] else ""
                    vcodec = f["codec"]
                    size = f" ({f['size_mb']}MB)" if f["size_mb"] > 0 else ""

                    # Highlight the format that would be selected
                    marker = (
                        " ← SELECTED"
                        if self._would_select_format(f, selected_quality)
                        else ""
                    )
                    color = Fore.LIGHTGREEN_EX if marker else ""
                    print(
                        f"  {color}{f['id']}: {height}p {ext} {vcodec}{fps} [{f['type']}]{size}{marker}{Style.RESET_ALL}"
                    )

            if audio_formats:
                print(f"\n{Fore.GREEN}AUDIO FORMATS:{Style.RESET_ALL}")
                for f in audio_formats[:5]:  # Show top 5
                    ext = f["ext"]
                    acodec = f["codec"]
                    abr = f" {f['abr']}kbps" if f["abr"] else ""
                    size = f" ({f['size_mb']}MB)" if f["size_mb"] > 0 else ""

                    # Highlight if audio-only mode
                    marker = (
                        " ← SELECTED" if audio_only and f == audio_formats[0] else ""
                    )
                    color = Fore.LIGHTGREEN_EX if marker else ""
                    print(
                        f"  {color}{f['id']}: {ext} {acodec}{abr}{size}{marker}{Style.RESET_ALL}"
                    )

        except Exception as e:
            print(f"{Fore.RED}Error listing formats: {e}{Style.RESET_ALL}")

    def _would_select_format(self, format_obj, quality):
        """Helper method to determine if a format would be selected based on quality setting"""
        if not quality or quality == "best":
            return (
                format_obj["type"] == "Video+Audio"
                and format_obj["height"]
                and format_obj["height"] > 0
            )

        height = format_obj["height"]
        if not height:
            return False

        quality_map = {
            "4k": 2160,
            "2160": 2160,
            "1440": 1440,
            "1080": 1080,
            "720": 720,
            "480": 480,
            "360": 360,
        }

        target_height = quality_map.get(quality)
        if target_height:
            return height == target_height and format_obj["type"] in [
                "Video+Audio",
                "Video Only",
            ]

        return False

    def get_video_info(self, url):
        """Get information about a YouTube video without downloading using the service"""
        try:
            info = self.service.get_video_info(url)

            print(f"{Fore.CYAN}Video Information:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Title:{Style.RESET_ALL} {info['title']}")
            print(f"{Fore.GREEN}Uploader:{Style.RESET_ALL} {info['uploader']}")
            duration = info["duration"]
            print(
                f"{Fore.GREEN}Duration:{Style.RESET_ALL} {duration // 60}:{duration % 60:02d}"
            )
            print(f"{Fore.GREEN}View Count:{Style.RESET_ALL} {info['view_count']:,}")
            print(f"{Fore.GREEN}Upload Date:{Style.RESET_ALL} {info['upload_date']}")
            print(
                f"{Fore.GREEN}Description:{Style.RESET_ALL} {info['description'][:200]}..."
            )

        except Exception as e:
            print(f"{Fore.RED}Error getting video info: {e}{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos using yt-dlp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py "https://www.youtube.com/watch?v=VIDEO_ID"
  python cli.py -i "https://www.youtube.com/watch?v=VIDEO_ID"  # Interactive mode
  python cli.py -q 1080 -o downloads "https://www.youtube.com/watch?v=VIDEO_ID"
  python cli.py -q 4k "https://www.youtube.com/watch?v=VIDEO_ID"
  python cli.py --audio-only --format mp3 "https://www.youtube.com/watch?v=VIDEO_ID"
  python cli.py --info "https://www.youtube.com/watch?v=VIDEO_ID"
  python cli.py --list-formats "https://www.youtube.com/watch?v=VIDEO_ID"

Note: For high quality videos (1080p+), FFmpeg is required to merge video and audio streams.
Use -i or --interactive for the best experience - you'll see all available options and can choose!
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
        "--list-formats",
        action="store_true",
        help="List all available formats for the video",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Interactive mode - choose format from available options",
    )

    args = parser.parse_args()

    # Validate URL
    if not ("youtube.com" in args.url or "youtu.be" in args.url):
        print(f"{Fore.RED}Error: Please provide a valid YouTube URL{Style.RESET_ALL}")
        sys.exit(1)

    downloader = YouTubeDownloaderCLI(args.output)

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
            interactive=args.interactive,
        )


if __name__ == "__main__":
    print(f"{Fore.MAGENTA}🎥 YouTube Video Downloader (CLI){Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'=' * 30}{Style.RESET_ALL}")
    main()
