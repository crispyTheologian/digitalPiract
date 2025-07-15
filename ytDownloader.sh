#!/usr/bin/env bash
#
#    A small script for downloading Youtube videos either as they are,
# or as .mp3 files for offline personal use.
#
#    Requires Firefox, for pulling cookies to validate with the
# server so we don't get kicked.
#
#
#     Usage:
#
#         music https://youtube.com/playlist=asdgfajf 25 120
#
#                                                            --simple as



music() {

    playlist="$1"                  # youtube link to playlist
    chunk=$2                       # download this many tracks before refreshing cookies
    pause=$3                       # wait this long between chunks
    conf="~/.config/yt-dlp/config" # configuration file containing other parameters.


    while true; do

      # yt-dlp download and convert to mp3; but continue even if it fails
      yt-dlp --config-location $conf --extract-audio --audio-format mp3 --max-downloads "$chunk" "$playlist"  || true
 
      # let the user know whats up when we stop after $chunk number of tracks for $pause number of seconds
      printf '\n[%(%F %T)T]  Pausing %ss and re‑loading fresh cookies …\n' -1 "$pause"

      # wait.
      sleep "$pause"

    done
}





video() {

    playlist="$1"                  # youtube link to playlist
    chunk=$2                       # download this many tracks before refreshing cookies
    pause=$3                       # wait this long between chunks
    conf="~/.config/yt-dlp/config" # configuration file containing other parameters.
    
    
    while true; do

      # typical yt-dlp download; but continue even if it fails
      yt-dlp --config-location "$conf" --max-downloads "$chunk" "$playlist"  || true

      # let the user know whats up when we stop after $chunk number of tracks for $pause number of seconds
      printf '\n[%(%F %T)T]  Pausing %ss and re‑loading fresh cookies …\n' -1 "$pause"

      # wait.
      sleep "$pause"
    done
}


webm2mp4() {
    ffmpeg -i "$1" -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 192k "$2"
}
