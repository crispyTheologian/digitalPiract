#!/usr/bin/env python3
"""
    Converts 1337 unicode text into plain english.
Requires: pip install unidecode
"""

import os.path import splitext
from re import sub as rSub
import sys
import unicodedata
import subprocess
import shlex
from pathlib import Path
from unidecode import unidecode as uDecode


# map out 1337 code characters actually used in files
dongles = str.maketrans({
    '0':'O', '1':'I', '2':'Z', '3':'E', '4':'A', '5':'S', '6':'G', '7':'T', '8':'B', '9':'g',
    '@':'A', '$':'S', '!':'I', '+':'T', '|':'I', '€':'E', '£':'L', '¥':'Y',
    '∆':'A', 'Δ':'A', 'Λ':'A', '▲':'A',
    'Σ':'E', 'Ξ':'E', 'Ω':'O', 'µ':'u',
    'Þ':'P', 'þ':'p', 'ß':'B',
    '₲':'G', '₡':'C', '¢':'C',
    'Ӿ':'X', 'Ж':'X', 'Я':'R', 'И':'N',
    '†':'T', '✝':'T',
})


# convert to ascii
def sanitise(name: str) -> str:
    """
    """

    stem, ext = splitext(name)
    stem = unicodedata.normalize(
        "NFKD", uDecode(stem).translate(dongles)
    )

    stem = rSub(r"[^A-Za-z0-9 ._()-]", "", stem)
    stem = rSub(r"\s+", " ", stem).strip()
    
    return f"{stem}{ext.lower()}"


# gather music files from the directory
def music_files(folder: Path):
    """
    """

    # i only use .mp3, but include others to be thorough
    extensions = {".mp3", ".flac", ".wav", ".aac", ".ogg", ".m4a", ".alac"}

    # return all files that actually are files and have matching extensions.
    return [ file for file in folder.rglob("*") \
             if  file.is_file() \
             and file.suffix.lower() \
             in extensions                        ]


# 4️⃣  Main logic – rename via `mv`
def main(root: Path):
    files = music_files(root)
    if not files:
        print("No music files found.")
        return

    print(f"🎵 Scanning {root.resolve()} — {len(files)} tracks found\n")

    for src in files:
        new_name = sanitise(src.name)
        if new_name == src.name:
            continue  # already clean

        dst = src.with_name(new_name)
        counter = 1
        while dst.exists():
            dst = src.with_name(rSub(r"(\.\w+)$", f" ({counter})\\1", new_name))
            counter += 1

        # Use `mv -- old new` to handle names beginning with dashes, etc.
        cmd = ["mv", "--", str(src), str(dst)]
        print("·", *map(shlex.quote, cmd[1:]))  # show the command (pretty)

        # Execute
        completed = subprocess.run(cmd, capture_output=True, text=True)
        if completed.returncode != 0:
            print("  ⚠️  mv failed:", completed.stderr.strip())

    print("\n✔ All renames attempted.")


# 5️⃣  Entry point
if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not target.is_dir():
        sys.exit(f"Not a directory: {target}")
    main(target)

