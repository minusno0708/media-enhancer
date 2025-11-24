import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ffmpeg_cmd import run as ffmpeg_run

def analyze(path):
    if not os.path.isfile(path):
        raise ValueError(f"The path {path} is not a valid file.")
    
    if not path.lower().endswith(('.mp4')):
        raise ValueError("The file is not an MP4 video.")

    try:
        result = ffmpeg_run("get_video_info.sh", path)
    except RuntimeError as e:
        print(f"Error retrieving video info: {e}")
        return
    
    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze video files.")
    parser.add_argument("-path", type=str, help="Path to the video file")
    args = parser.parse_args()

    analyze(args.path)