#!/usr/bin/env python3
"""
YouTube Video Downloader Launcher
Choose between CLI and GUI versions
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description="YouTube Video Downloader - Choose your interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Interface Options:
  --gui, -g     Launch GUI version (graphical interface)
  --cli, -c     Launch CLI version (command line interface)
  
If no interface is specified, GUI will be launched by default.

Examples:
  python launcher.py --gui
  python launcher.py --cli "https://www.youtube.com/watch?v=VIDEO_ID"
  python launcher.py -c -i "https://www.youtube.com/watch?v=VIDEO_ID"  # CLI interactive mode
        """,
    )

    parser.add_argument("--gui", "-g", action="store_true", help="Launch GUI version")

    parser.add_argument("--cli", "-c", action="store_true", help="Launch CLI version")

    # Parse known args to allow CLI arguments to pass through
    args, unknown = parser.parse_known_args()

    # If both or neither specified, default to GUI
    if args.gui or not args.cli:
        print("🎥 Launching YouTube Downloader GUI...")
        try:
            import gui

            gui.main()
        except ImportError as e:
            print(f"Error importing GUI modules: {e}")
            print("Make sure all required packages are installed.")
            sys.exit(1)
        except Exception as e:
            print(f"Error launching GUI: {e}")
            sys.exit(1)

    elif args.cli:
        print("🎥 Launching YouTube Downloader CLI...")
        try:
            import cli

            # Reconstruct sys.argv for the CLI app
            sys.argv = ["cli.py"] + unknown
            cli.main()
        except ImportError as e:
            print(f"Error importing CLI modules: {e}")
            print("Make sure all required packages are installed.")
            sys.exit(1)
        except SystemExit:
            # Normal exit from CLI app
            pass
        except Exception as e:
            print(f"Error launching CLI: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
