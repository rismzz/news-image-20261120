#!/usr/bin/env python3
"""Copy the 20 November 2026 broadsheet into the grader's output dir.

The poster itself is entry.png next to this file, rendered ahead of
time by render_frontpage.py. This entrypoint only checks the file
is a PNG of at most 1024x1024 px and at most 1 MiB, then copies it
to $MAKEFUN_OUTPUT_DIR/entry.png (default /output). Standard
library only, no network, no clock, no randomness: two runs write
identical bytes.
"""

import hashlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
POSTER = HERE / "entry.png"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024
MAGIC = b"\x89PNG\r\n\x1a\n"
CHUNK = 65536


def die(msg):
    print(f"main.py: {msg}", file=sys.stderr)
    return 1


def png_side(path):
    """Return (width, height) from the IHDR chunk, or None if unreadable."""
    with path.open("rb") as fh:
        head = fh.read(24)
    if len(head) < 24 or head[:8] != MAGIC or head[12:16] != b"IHDR":
        return None
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    return width, height


def main():
    if not POSTER.is_file():
        return die("entry.png is missing from the repository")
    size = POSTER.stat().st_size
    if size > MAX_BYTES:
        return die(f"entry.png is {size} bytes, over the 1 MiB cap")
    sides = png_side(POSTER)
    if sides is None:
        return die("entry.png is not a readable PNG file")
    if sides[0] > MAX_SIDE or sides[1] > MAX_SIDE:
        return die(f"entry.png is {sides[0]}x{sides[1]}, over the 1024 cap")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    digest = hashlib.sha256()
    with POSTER.open("rb") as src, dest.open("wb") as dst:
        while True:
            block = src.read(CHUNK)
            if not block:
                break
            digest.update(block)
            dst.write(block)
    if dest.stat().st_size != size:
        return die("copied entry.png came out short")
    check = hashlib.sha256(dest.read_bytes()).hexdigest()
    if check != digest.hexdigest():
        return die("copied entry.png failed its sha256 check")
    print(f"wrote {dest} ({size} bytes, sha256 {digest.hexdigest()[:16]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
