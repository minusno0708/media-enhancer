#!/bin/bash

FRAMES_PATTERN="$1"
FPS="$2"
OUTPUT="$3"
OPTIONS="$4"

if [ -z "$FRAMES_PATTERN" ] || [ -z "$FPS" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 <frames_pattern> <fps> <output_file>"
    exit 2
fi

ffmpeg -y -framerate "$FPS" -i "$FRAMES_PATTERN" -c:v libx264 -r "$FPS" $OPTIONS "$OUTPUT"