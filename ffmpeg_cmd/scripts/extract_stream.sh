#!/bin/bash

SOURCE="$1"
INDEX="$2"
OUTPUT="$3"

if [ -z "$SOURCE" ] || [ -z "$INDEX" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 <source_file> <stream_index> <stream_type> <output_file>"
    exit 2
fi

ffmpeg -i "$SOURCE" -map 0:"$INDEX" -c copy "$OUTPUT"