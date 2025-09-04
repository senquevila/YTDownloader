#!/usr/bin/env python3
"""
YouTube Video Downloader - GUI Version
A graphical user interface for the YouTube video downloader using tkinter
"""

import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

from downloader_service import YouTubeDownloaderService


class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎥 YouTube Video Downloader")
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Variables
        self.url_var = tk.StringVar()
        self.output_dir_var = tk.StringVar(value=str(Path.cwd() / "downloads"))
        self.download_mode_var = tk.StringVar(value="video")
        self.selected_format = None
        self.formats_data = []
        self.service = YouTubeDownloaderService()

        self.setup_ui()

    def setup_ui(self):
        """Setup the main user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame, text="🎥 YouTube Video Downloader", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # URL input section
        url_frame = ttk.LabelFrame(main_frame, text="Video URL", padding="10")
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(1, weight=1)

        ttk.Label(url_frame, text="URL:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10)
        )
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))

        self.get_info_btn = ttk.Button(
            url_frame, text="Get Video Info", command=self.get_video_info
        )
        self.get_info_btn.grid(row=0, column=2)

        # Video info section
        info_frame = ttk.LabelFrame(main_frame, text="Video Information", padding="10")
        info_frame.grid(
            row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        info_frame.columnconfigure(0, weight=1)

        self.info_text = scrolledtext.ScrolledText(info_frame, height=4, width=70)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Download options section
        options_frame = ttk.LabelFrame(
            main_frame, text="Download Options", padding="10"
        )
        options_frame.grid(
            row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        options_frame.columnconfigure(1, weight=1)

        # Download mode
        ttk.Label(options_frame, text="Mode:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10)
        )
        mode_frame = ttk.Frame(options_frame)
        mode_frame.grid(row=0, column=1, sticky=tk.W)

        ttk.Radiobutton(
            mode_frame,
            text="Video",
            variable=self.download_mode_var,
            value="video",
            command=self.on_mode_change,
        ).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(
            mode_frame,
            text="Audio Only",
            variable=self.download_mode_var,
            value="audio",
            command=self.on_mode_change,
        ).pack(side=tk.LEFT)

        # Output directory
        ttk.Label(options_frame, text="Output:").grid(
            row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0)
        )
        output_frame = ttk.Frame(options_frame)
        output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(10, 0))
        output_frame.columnconfigure(0, weight=1)

        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        ttk.Button(output_frame, text="Browse", command=self.browse_output_dir).grid(
            row=0, column=1
        )

        # Format selection section
        format_frame = ttk.LabelFrame(
            main_frame, text="Available Formats", padding="10"
        )
        format_frame.grid(
            row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )
        format_frame.columnconfigure(0, weight=1)
        format_frame.rowconfigure(1, weight=1)

        # Format selection buttons
        format_btn_frame = ttk.Frame(format_frame)
        format_btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        self.load_formats_btn = ttk.Button(
            format_btn_frame, text="Load Available Formats", command=self.load_formats
        )
        self.load_formats_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.refresh_btn = ttk.Button(
            format_btn_frame,
            text="Refresh",
            command=self.refresh_formats,
            state="disabled",
        )
        self.refresh_btn.pack(side=tk.LEFT)

        # Format list
        list_frame = ttk.Frame(format_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Create treeview for formats
        columns = ("Type", "Quality", "Format", "Codec", "Size")
        self.format_tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", height=8
        )

        # Configure columns
        self.format_tree.heading("Type", text="Type")
        self.format_tree.heading("Quality", text="Quality")
        self.format_tree.heading("Format", text="Format")
        self.format_tree.heading("Codec", text="Codec")
        self.format_tree.heading("Size", text="Size (MB)")

        self.format_tree.column("Type", width=100)
        self.format_tree.column("Quality", width=100)
        self.format_tree.column("Format", width=80)
        self.format_tree.column("Codec", width=100)
        self.format_tree.column("Size", width=80)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.format_tree.yview
        )
        self.format_tree.configure(yscrollcommand=scrollbar.set)

        self.format_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Bind selection event
        self.format_tree.bind("<<TreeviewSelect>>", self.on_format_select)

        # Download section
        download_frame = ttk.LabelFrame(main_frame, text="Download", padding="10")
        download_frame.grid(
            row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        download_frame.columnconfigure(0, weight=1)

        # Progress bar
        self.progress_var = tk.StringVar(value="Ready to download")
        ttk.Label(download_frame, textvariable=self.progress_var).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )

        self.progress_bar = ttk.Progressbar(download_frame, mode="indeterminate")
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Download button
        self.download_btn = ttk.Button(
            download_frame,
            text="Download Selected Format",
            command=self.start_download,
            state="disabled",
        )
        self.download_btn.grid(row=2, column=0)

        # Configure grid weights for resizing
        main_frame.rowconfigure(4, weight=1)

    def get_video_info(self):
        """Get and display video information"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a YouTube URL")
            return

        if not ("youtube.com" in url or "youtu.be" in url):
            messagebox.showerror("Error", "Please provide a valid YouTube URL")
            return

        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "Loading video information...")
        self.get_info_btn.config(state="disabled")

        def fetch_info():
            try:
                info = self.service.get_video_info(url)
                # Update UI in main thread
                self.root.after(0, lambda: self.display_video_info(info))

            except Exception as e:
                self.root.after(
                    0, lambda: self.show_error(f"Error getting video info: {str(e)}")
                )
            finally:
                self.root.after(0, lambda: self.get_info_btn.config(state="normal"))

        # Run in separate thread
        threading.Thread(target=fetch_info, daemon=True).start()

    def display_video_info(self, info):
        """Display video information in the text widget"""
        self.info_text.delete(1.0, tk.END)

        title = info.get("title", "N/A")
        uploader = info.get("uploader", "N/A")
        duration = info.get("duration", 0)
        view_count = info.get("view_count", 0)
        upload_date = info.get("upload_date", "N/A")

        info_text = f"""Title: {title}
Uploader: {uploader}
Duration: {duration // 60}:{duration % 60:02d}
Views: {view_count:,}
Upload Date: {upload_date}"""

        self.info_text.insert(tk.END, info_text)

        # Enable format loading
        self.load_formats_btn.config(state="normal")
        self.refresh_btn.config(state="normal")

    def load_formats(self):
        """Load available formats for the video"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a YouTube URL first")
            return

        self.progress_var.set("Loading available formats...")
        self.progress_bar.start()
        self.load_formats_btn.config(state="disabled")

        def fetch_formats():
            try:
                formats = self.service.get_available_formats(url)
                # Update UI in main thread
                self.root.after(0, lambda: self.display_formats(formats))

            except Exception as e:
                self.root.after(
                    0, lambda: self.show_error(f"Error loading formats: {str(e)}")
                )
            finally:
                self.root.after(0, lambda: self.finish_loading_formats())

        # Run in separate thread
        threading.Thread(target=fetch_formats, daemon=True).start()

    def display_formats(self, formats):
        """Display formats in the treeview"""
        # Clear existing items
        for item in self.format_tree.get_children():
            self.format_tree.delete(item)

        self.formats_data = formats

        # Add formats to treeview
        for fmt in formats:
            size_mb = str(fmt["size_mb"]) if fmt["size_mb"] > 0 else ""

            self.format_tree.insert(
                "",
                tk.END,
                values=(
                    fmt["type"],
                    fmt["quality"],
                    fmt["ext"],
                    fmt["codec"][:15] if fmt["codec"] else "",
                    size_mb,
                ),
            )

        self.progress_var.set(f"Found {len(formats)} available formats")

    def finish_loading_formats(self):
        """Finish loading formats and update UI"""
        self.progress_bar.stop()
        self.load_formats_btn.config(state="normal")

    def refresh_formats(self):
        """Refresh the formats list"""
        self.load_formats()

    def on_format_select(self, event):
        """Handle format selection"""
        selection = self.format_tree.selection()
        if selection:
            item = selection[0]
            index = self.format_tree.index(item)
            self.selected_format = self.formats_data[index]
            self.download_btn.config(state="normal")
            self.progress_var.set(
                f"Selected: {self.selected_format['type']} - {self.selected_format['quality']}"
            )

    def on_mode_change(self):
        """Handle download mode change"""
        # Clear format selection when mode changes
        self.format_tree.selection_remove(self.format_tree.selection())
        self.selected_format = None
        self.download_btn.config(state="disabled")
        self.progress_var.set("Mode changed - please select a format")

    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)

    def start_download(self):
        """Start the download process"""
        if not self.selected_format:
            messagebox.showwarning("Warning", "Please select a format first")
            return

        url = self.url_var.get().strip()
        output_dir = self.output_dir_var.get().strip()

        if not url:
            messagebox.showwarning("Warning", "Please enter a YouTube URL")
            return

        if not output_dir:
            messagebox.showwarning("Warning", "Please specify an output directory")
            return

        # Disable download button and start progress
        self.download_btn.config(state="disabled")
        self.progress_bar.start()
        self.progress_var.set("Downloading...")

        def download():
            try:
                # Set output directory for the service
                self.service.set_output_directory(output_dir)

                # Determine download parameters based on selected format
                if self.selected_format["type"] == "Audio Only":
                    audio_only = True
                    quality = "best"
                    output_format = self.selected_format["ext"]
                else:
                    audio_only = False
                    quality = (
                        str(self.selected_format["height"])
                        if self.selected_format["height"]
                        else "best"
                    )
                    output_format = None

                # Progress callback for GUI
                def progress_hook(d):
                    if d["status"] == "downloading":
                        # Update progress in main thread
                        self.root.after(
                            0,
                            lambda: self.progress_var.set(
                                f"Downloading... {d.get('_percent_str', 'N/A')}"
                            ),
                        )
                    elif d["status"] == "finished":
                        self.root.after(
                            0, lambda: self.progress_var.set("Processing...")
                        )

                # Download using the service
                result = self.service.download_video(
                    url=url,
                    quality=quality,
                    audio_only=audio_only,
                    output_format=output_format,
                    progress_callback=progress_hook,
                )

                # Success
                self.root.after(0, lambda: self.download_complete())

            except Exception as e:
                self.root.after(0, lambda: self.download_error(str(e)))

        # Run download in separate thread
        threading.Thread(target=download, daemon=True).start()

    def download_complete(self):
        """Handle successful download completion"""
        self.progress_bar.stop()
        self.download_btn.config(state="normal")
        self.progress_var.set("Download completed successfully!")
        messagebox.showinfo("Success", "Download completed successfully!")

    def download_error(self, error_msg):
        """Handle download error"""
        self.progress_bar.stop()
        self.download_btn.config(state="normal")
        self.progress_var.set("Download failed")
        messagebox.showerror("Download Error", f"Download failed:\n{error_msg}")

    def show_error(self, message):
        """Show error message"""
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, message)
        messagebox.showerror("Error", message)


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)

    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nGUI closed by user")


if __name__ == "__main__":
    print("🎥 Starting YouTube Video Downloader GUI...")
    main()
