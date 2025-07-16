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
        Translate and convert all look-alike unicode
    charactes to their plain english counterparts;
    drop anything else that is not recognized as an
    alphanumeric character.
    """

    stem, ext = splitext(name)
    stem = unicodedata.normalize(
        "NFKD", uDecode(stem).translate(dongles)
    )

    stem = rSub(r"[^A-Za-z0-9 ._()-]", "", stem)
    stem = rSub(r"\s+", " ", stem).strip()
    
    return f"{stem}{ext.lower()}"


def music_files(folder: Path):
    """
        Glob music files from a directory and return
    all files that are actually files and have musical
    file extensions.

    As a rule, I stick to Mp3 files but I have included
    other formats in an effort to be thorough.
    """

    extensions = { ".mp3", ".flac", ".wav",
                   ".aac", ".ogg",  ".m4a",
                   ".alac"                  }

    return [ file for file in folder.rglob("*") \
              if  file.is_file() \
              and file.suffix.lower() \
              in extensions                       ]


def main(root: Path):
    """
    Sanitizes music file names in the given directory by
    converting fancy/Unicode/leet characters into plain
    English, then renames the files accordingly.
    
    Arguments:
        root (Path): The directory to scan for music files.
    """

    # enumerate files in our library
    files = music_files(root)

    # make sure we aren't in an empty directory
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

        # create a new filepath based on the new name
        dst = track.with_name(newName)

        # begin counting for namespace collisions
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

    # inform success, if possible
    print( "\n✔ All renames attempted." )


if __name__ == "__main__":

    target = Path(sys.argv[1]) \
        if len(sys.argv) > 1 \
        else Path.cwd()

    if not target.is_dir():
        sys.exit( f"Not a directory: {target}" )
    main(target)

