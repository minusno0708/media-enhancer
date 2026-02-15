import argparse
import os
import shutil
import sys
from unittest import result

from analyzer import analyze

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ffmpeg_cmd import run as ffmpeg_run    

def extract_streams(filepath, output, streams):
    stream_files = {}

    for stream in streams:
        index = stream.get('index')

        if stream.get('codec_type') == 'video':
            output_filename = f"{output}/stream_{index}.mp4"
        elif stream.get('codec_type') == 'audio':
            output_filename = f"{output}/stream_{index}.m4a"

        try:
            ffmpeg_run("extract_stream.sh", filepath, index, output_filename)
            stream_files[index] = output_filename
            print(f"Successfully extracted stream {index} to {output_filename}")
        except RuntimeError as e:
            print(f"Error extracting stream {index}: {e}")
    print("Successfully extracted all streams.")

    return stream_files

def extract_videos(filepath, output):
    if not os.path.exists(output):
        os.makedirs(output)

    try:
        ffmpeg_run("extract_frames.sh", filepath, output)
        print(f"Successfully extracted frames from {filepath} to {output}")
    except RuntimeError as e:
        print(f"Error extracting frames from {filepath}: {e}")

def extract(filepath, output):
    streams = analyze(filepath)

    if not os.path.exists(output):
        os.makedirs(output)
    
    stream_files = extract_streams(filepath, output, streams)
    
    for stream in streams:
        index = stream.get('index')
        codec_type = stream.get('codec_type')

        if codec_type == 'video':
            extract_videos(stream_files[index], f"{output}/frames_{index}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract streams from a video file.")
    parser.add_argument("-f", "--file", type=str, required=True, help="Input Path")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output Path")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output directory")

    args = parser.parse_args()

    if args.overwrite and os.path.exists(args.output):
        shutil.rmtree(args.output)
    
    extract(args.file, args.output)