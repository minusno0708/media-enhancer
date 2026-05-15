#!/bin/bash

VIDEO_STREAM="$1"
AUDIO_STREAM="$2"
OUTPUT="$3"

if [ -z "$VIDEO_STREAM" ] || [ -z "$AUDIO_STREAM" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 <video_stream> <audio_stream> <output_file>"
    exit 2
fi

ffmpeg -y -i "$VIDEO_STREAM" -i "$AUDIO_STREAM" "$OUTPUT"