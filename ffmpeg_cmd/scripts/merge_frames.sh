#!/bin/bash

FRAMES_PATTERN="$1"
FPS="$2"
OUTPUT="$3"

if [ -z "$FRAMES_PATTERN" ] || [ -z "$FPS" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 <fps> <frame_pattern> <output_file>"
    exit 2
fi

ffmpeg -y -r "$FPS" -i "$FRAMES_PATTERN" -c:v copy "$OUTPUT"