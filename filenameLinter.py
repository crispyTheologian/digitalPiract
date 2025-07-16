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
dongles = str.maketrans(
    { '0':'O', '1':'I', '2':'Z',
      '3':'E', '4':'A', '5':'S',
      '6':'G', '7':'T', '8':'B',
      '9':'g', '@':'A', '$':'S',
      '!':'I', '+':'T', '|':'I',
      '€':'E', '£':'L', '¥':'Y',
      '∆':'A', 'Δ':'A', 'Λ':'A',
      '▲':'A', 'Σ':'E', 'Ξ':'E',
      'Ω':'O', 'µ':'u', 'Þ':'P',
      'þ':'p', 'ß':'B', '₲':'G',
      '₡':'C', '¢':'C', 'Ӿ':'X',
      'Ж':'X', 'Я':'R', 'И':'N',
      '†':'T', '✝':'T',          }
)


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
              in extensions                       ]


# 4️⃣  Main logic – rename via `mv`
def main(root: Path):
    files = music_files(root)
    if not files:
        print( "No music files found." )
        return

    # otherwise, show how many files we found
    print( f"@: Scanning {root.resolve()} — "
           f"{len(files)} tracks found\n"     )

    # begin looping through tracks
    for track in files:
        
        # translate filenames using our function
        newName = sanitise(track.name)
        
        # skip the ones that are already clean
        if newName == track.name:
            continue

        dst = src.with_name(new_name)
        counter = 1
        while dst.exists():
            
            # append a number if collision occurs
            dst = track.with_name(
                rSub( r"(\.\w+)$",
                      f" ({counter})\\1",
                      new_name            )
            ); counter += 1# increment 

        # formulate shell command to rename tracks
        cmd = ["mv", "--", str(track), str(dst)]

        # display command to be executed
        print("·", *map(shlex.quote, cmd[1:]))

        # execute the command
        completed = subprocess.run(
            cmd, capture_output=True,
            text=True
        )
        
        # return error, if any
        if completed.returncode != 0:
            print( "  ⚠️  mv failed:",
                   completed.stderr.strip() )

    print("\n✔ All renames attempted.")


# 5️⃣  Entry point
if __name__ == "__main__":

    target = Path(sys.argv[1]) \
        if len(sys.argv) > 1 \
        else Path.cwd()

    if not target.is_dir():
        sys.exit( f"Not a directory: {target}" )
    main(target)

