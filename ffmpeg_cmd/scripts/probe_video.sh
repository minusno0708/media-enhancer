#!/bin/bash

FILE="$1"

if [ -z "$FILE" ]; then
	echo "Usage: $0 <file>"
	exit 2
fi

ffprobe -v error -show_format -show_streams -i "$FILE"