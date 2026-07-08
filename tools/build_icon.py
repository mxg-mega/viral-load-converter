#!/usr/bin/env python3
"""Generate a Windows .ico from resources/app_icon.png.

Windows .ico files are required by Inno Setup's SetupIconFile and the
Windows Explorer's icon system. The source PNG is 70x70; we embed it at
multiple standard sizes (16, 32, 48, 64, 128, 256) so the result looks
sharp at any DPI / Start Menu / Taskbar / shortcut context.

Usage:
    python tools/build_icon.py

Output:
    resources/app_icon.ico
"""
from pathlib import Path
import sys

try:
    from PIL import Image
except ImportError:
    print("Pillow is required: pip install pillow", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "resources" / "app_icon.png"
DST = ROOT / "resources" / "app_icon.ico"

SIZES = [16, 32, 48, 64, 128, 256]


def main() -> int:
    if not SRC.exists():
        print(f"Source icon not found: {SRC}", file=sys.stderr)
        return 1

    img = Image.open(SRC)
    # Pillow needs RGBA for .ico with transparency; convert if needed.
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Build a multi-resolution .ico. The first size is the one Windows
    # uses by default; the rest are included for HiDPI.
    base = img.resize((SIZES[0], SIZES[0]), Image.LANCZOS)
    others = [img.resize((s, s), Image.LANCZOS) for s in SIZES[1:]]
    base.save(DST, format="ICO", sizes=[(s, s) for s in SIZES], append_images=others)

    print(f"Wrote {DST} ({DST.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
