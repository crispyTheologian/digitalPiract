#!/usr/bin/env bash
#
#    A small script for downloading Youtube videos as .mp3 files for
# offline, personal use.
#
#    Requires Firefox, for pulling cookies to validate with the
# server so we don't get kicked.
#
#     Usage:
#
#         downloadMusic https://youtube.com/playlist=asdgfajf
#
#                                                            --simple as


playlist="$1"                  # youtube link to playlist
chunk=25                       # download this many tracks before refreshing cookies
pause=120                      # wait this long between chunks
conf="~/.config/yt-dlp/config" # configuration file containing other parameters.


while true; do

  # typical yt-dlp download; but continue even if it fails
  yt-dlp --config-location $conf --extract-audio --audio-format mp3 --max-downloads "$chunk" "$playlist"  || true

  # let the user know whats up when we stop after $chunk number of tracks for $pause number of seconds
  printf '\n[%(%F %T)T]  Pausing %ss and re‑loading fresh cookies …\n' -1 "$pause"

  # wait.
  sleep "$pause"

done




