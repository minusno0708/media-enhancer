#!/bin/bash

SOURCE="$1"
OUTPUT="$2"

if [ -z "$SOURCE" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 <source_file> <output_directory>"
    exit 2
fi

ffmpeg -i "$SOURCE" "$OUTPUT/frame_%04d.png"