#!/usr/bin/env python3
"""
YouTube Downloader Service
Centralized service for handling YouTube video downloads, format selection, and video information
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yt_dlp


class YouTubeDownloaderService:
    """
    Centralized service for YouTube video downloading functionality.
    This service handles all the core logic for downloads, format selection, and video information.
    """

    def __init__(self, output_dir: str = "downloads"):
        """
        Initialize the downloader service

        Args:
            output_dir (str): Default output directory for downloads
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def set_output_directory(self, output_dir: str) -> None:
        """Set a new output directory"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def validate_url(self, url: str) -> bool:
        """
        Validate if the URL is a valid YouTube URL

        Args:
            url (str): YouTube video URL

        Returns:
            bool: True if valid YouTube URL, False otherwise
        """
        return bool(url and ("youtube.com" in url or "youtu.be" in url))

    def get_video_info(self, url: str) -> Dict[str, Any]:
        """
        Get detailed information about a YouTube video

        Args:
            url (str): YouTube video URL

        Returns:
            Dict[str, Any]: Video information dictionary

        Raises:
            Exception: If unable to extract video information
        """
        if not self.validate_url(url):
            raise ValueError("Invalid YouTube URL")

        try:
            ydl_opts = {"quiet": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                return {
                    "title": info.get("title", "N/A"),
                    "uploader": info.get("uploader", "N/A"),
                    "duration": info.get("duration", 0),
                    "view_count": info.get("view_count", 0),
                    "upload_date": info.get("upload_date", "N/A"),
                    "description": info.get("description", "N/A"),
                    "thumbnail": info.get("thumbnail", ""),
                    "webpage_url": info.get("webpage_url", url),
                    "id": info.get("id", ""),
                    "formats": info.get("formats", []),
                }
        except Exception as e:
            raise Exception(f"Error getting video info: {str(e)}")

    def get_available_formats(self, url: str) -> List[Dict[str, Any]]:
        """
        Get all available formats for a YouTube video, organized and processed

        Args:
            url (str): YouTube video URL

        Returns:
            List[Dict[str, Any]]: List of processed format information

        Raises:
            Exception: If unable to extract format information
        """
        try:
            video_info = self.get_video_info(url)
            formats = video_info.get("formats", [])

            processed_formats = []

            for f in formats:
                format_info = {
                    "id": f.get("format_id"),
                    "ext": f.get("ext", "unknown"),
                    "vcodec": f.get("vcodec", "none"),
                    "acodec": f.get("acodec", "none"),
                    "height": f.get("height"),
                    "width": f.get("width"),
                    "fps": f.get("fps"),
                    "filesize": f.get("filesize"),
                    "abr": f.get("abr"),
                    "format_note": f.get("format_note", ""),
                    "url": f.get("url", ""),
                    "raw_format": f,
                }

                # Determine type
                if format_info["vcodec"] != "none" and format_info["acodec"] != "none":
                    format_info["type"] = "Video+Audio"
                elif format_info["vcodec"] != "none":
                    format_info["type"] = "Video Only"
                elif format_info["acodec"] != "none":
                    format_info["type"] = "Audio Only"
                else:
                    continue

                # Quality description
                if format_info["height"]:
                    format_info["quality"] = f"{format_info['height']}p"
                    if format_info["fps"]:
                        format_info["quality"] += f" {format_info['fps']}fps"
                elif format_info["abr"]:
                    format_info["quality"] = f"{format_info['abr']}kbps"
                else:
                    format_info["quality"] = "Unknown"

                # Codec info
                if format_info["type"] == "Audio Only":
                    format_info["codec"] = format_info["acodec"]
                else:
                    format_info["codec"] = format_info["vcodec"]

                # File size in MB
                if format_info["filesize"]:
                    format_info["size_mb"] = format_info["filesize"] // 1024 // 1024
                else:
                    format_info["size_mb"] = 0

                processed_formats.append(format_info)

            # Sort by type and quality
            def sort_key(fmt):
                type_priority = {"Video+Audio": 0, "Video Only": 1, "Audio Only": 2}
                height = fmt["height"] or 0
                return (type_priority.get(fmt["type"], 3), -height)

            processed_formats.sort(key=sort_key)

            return processed_formats

        except Exception as e:
            raise Exception(f"Error getting available formats: {str(e)}")

    def get_format_selection_options(self, url: str) -> List[Dict[str, Any]]:
        """
        Get organized format options for interactive selection

        Args:
            url (str): YouTube video URL

        Returns:
            List[Dict[str, Any]]: List of selectable format options
        """
        try:
            formats = self.get_available_formats(url)

            options = []
            option_num = 1

            # Video formats - group by resolution to avoid duplicates
            video_formats = [
                f for f in formats if f["type"] in ["Video+Audio", "Video Only"]
            ]
            resolutions_shown = set()

            for fmt in video_formats:
                height = fmt["height"]
                if height and height not in resolutions_shown:
                    resolutions_shown.add(height)
                    options.append(
                        {
                            "num": option_num,
                            "type": "video",
                            "quality": str(height),
                            "audio_only": False,
                            "description": f"{height}p {fmt['ext']} {fmt['codec'][:10]}",
                            "format_info": fmt,
                        }
                    )
                    option_num += 1

            # Audio formats - show top 3 unique options
            audio_formats = [f for f in formats if f["type"] == "Audio Only"]
            audio_shown = set()

            for fmt in audio_formats[:3]:
                format_key = f"{fmt['acodec']}_{fmt['ext']}_{fmt['abr']}"
                if format_key not in audio_shown:
                    audio_shown.add(format_key)
                    options.append(
                        {
                            "num": option_num,
                            "type": "audio",
                            "quality": "best",
                            "audio_only": True,
                            "output_format": fmt["ext"],
                            "description": f"Audio {fmt['ext']} {fmt['acodec']} {fmt['abr']}kbps",
                            "format_info": fmt,
                        }
                    )
                    option_num += 1

            return options

        except Exception as e:
            raise Exception(f"Error getting format selection options: {str(e)}")

    def get_download_options(
        self,
        quality: str = "best",
        audio_only: bool = False,
        output_format: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get yt-dlp download options based on quality settings

        Args:
            quality (str): Video quality preference
            audio_only (bool): Download audio only
            output_format (str): Output format override

        Returns:
            Dict[str, Any]: yt-dlp options dictionary
        """
        ydl_opts = {
            "outtmpl": str(self.output_dir / "%(title)s.%(ext)s"),
            "noplaylist": True,
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
            # Video format selection with audio
            if quality == "best":
                ydl_opts["format"] = (
                    "bestvideo[height<=2160]+bestaudio/best[height<=2160]/bestvideo+bestaudio/best"
                )
            elif quality == "worst":
                ydl_opts["format"] = "worst"
            elif quality == "4k" or quality == "2160":
                ydl_opts["format"] = (
                    "bestvideo[height<=2160]+bestaudio/best[height<=2160]/best[height<=2160]"
                )
            elif quality == "1440":
                ydl_opts["format"] = (
                    "bestvideo[height<=1440]+bestaudio/best[height<=1440]/best[height<=1440]"
                )
            elif quality == "1080":
                ydl_opts["format"] = (
                    "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best[height<=1080]"
                )
            elif quality == "720":
                ydl_opts["format"] = (
                    "bestvideo[height<=720]+bestaudio/best[height<=720]/best[height<=720]"
                )
            elif quality == "480":
                ydl_opts["format"] = (
                    "bestvideo[height<=480]+bestaudio/best[height<=480]/best[height<=480]"
                )
            elif quality == "360":
                ydl_opts["format"] = (
                    "bestvideo[height<=360]+bestaudio/best[height<=360]/best[height<=360]"
                )
            else:
                # For custom quality
                ydl_opts["format"] = (
                    f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best[height<={quality}]"
                )

            # Add video format conversion if specified
            if output_format:
                ydl_opts["postprocessors"] = [
                    {
                        "key": "FFmpegVideoConvertor",
                        "preferedformat": output_format,
                    }
                ]

        return ydl_opts

    def download_video(
        self,
        url: str,
        quality: str = "best",
        audio_only: bool = False,
        output_format: Optional[str] = None,
        progress_callback: Optional[callable] = None,
    ) -> Dict[str, Any]:
        """
        Download a YouTube video with specified options

        Args:
            url (str): YouTube video URL
            quality (str): Video quality preference
            audio_only (bool): Download audio only
            output_format (str): Output format override
            progress_callback (callable): Optional callback for progress updates

        Returns:
            Dict[str, Any]: Download result information

        Raises:
            Exception: If download fails
        """
        if not self.validate_url(url):
            raise ValueError("Invalid YouTube URL")

        try:
            # Get download options
            ydl_opts = self.get_download_options(quality, audio_only, output_format)

            # Add progress hook if provided
            if progress_callback:
                ydl_opts["progress_hooks"] = [progress_callback]

            # Get video info first
            info = self.get_video_info(url)

            # Perform the download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            return {
                "success": True,
                "title": info["title"],
                "uploader": info["uploader"],
                "duration": info["duration"],
                "output_dir": str(self.output_dir.absolute()),
                "quality": quality,
                "audio_only": audio_only,
                "message": "Download completed successfully!",
            }

        except yt_dlp.DownloadError as e:
            raise Exception(f"Download Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected Error: {str(e)}")

    def preview_download(
        self, url: str, quality: str = "best", audio_only: bool = False
    ) -> Dict[str, Any]:
        """
        Preview what would be downloaded without actually downloading

        Args:
            url (str): YouTube video URL
            quality (str): Video quality preference
            audio_only (bool): Download audio only

        Returns:
            Dict[str, Any]: Preview information
        """
        try:
            info = self.get_video_info(url)
            ydl_opts = self.get_download_options(quality, audio_only)

            return {
                "title": info["title"],
                "uploader": info["uploader"],
                "duration": info["duration"],
                "output_dir": str(self.output_dir.absolute()),
                "quality_setting": quality,
                "audio_only": audio_only,
                "format_string": ydl_opts.get("format", "default"),
                "estimated_filename": f"{info['title']}.{'mp3' if audio_only else 'mp4'}",
            }

        except Exception as e:
            raise Exception(f"Error previewing download: {str(e)}")


# Quality constants for easy access
QUALITY_OPTIONS = {
    "best": "Best quality available (up to 4K)",
    "4k": "4K Ultra HD (2160p)",
    "2160": "4K Ultra HD (2160p)",
    "1440": "2K Quad HD (1440p)",
    "1080": "Full HD (1080p)",
    "720": "HD Ready (720p)",
    "480": "Standard Definition (480p)",
    "360": "Low Quality (360p)",
    "worst": "Lowest quality available",
}

SUPPORTED_FORMATS = {
    "video": ["mp4", "webm", "mkv", "avi"],
    "audio": ["mp3", "m4a", "wav", "flac", "ogg"],
}
