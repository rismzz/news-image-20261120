#!/usr/bin/env python3
"""Entrypoint for the news-image-20261120 entry.

Verifies the bundled entry.png (PNG magic bytes, IHDR size at most
1024x1024, file at most 1 MiB) and copies it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output). Standard library
only, no network. Deterministic: two runs write identical bytes.
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
MAX_DIM = 1024


def fail(msg):
    print("main.py: ERROR: %s" % msg, file=sys.stderr)
    sys.exit(1)


def verify_png(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("entry.png lacks the PNG magic bytes")
    if len(data) < 33 or data[12:16] != b"IHDR":
        fail("entry.png lacks an IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        fail("entry.png is %dx%d, over the 1024x1024 limit" % (width, height))
    return hashlib.sha256(data).hexdigest(), len(data)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    digest, size = verify_png(SRC)
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    with open(dest, "rb") as fh:
        copied = hashlib.sha256(fh.read()).hexdigest()
    if copied != digest:
        fail("copied entry.png hash mismatch: %s != %s" % (copied, digest))
    print("main.py: verified entry.png (%d bytes, sha256 %s)" % (size, digest))
    print("main.py: wrote %s (sha256 match)" % dest)


if __name__ == "__main__":
    main()
