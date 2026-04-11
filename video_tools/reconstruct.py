import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import video_tools
import ffmpeg_cmd

def merge_frames(dir, metadata, output):
    frames_pattern = os.path.join(dir, "frame_%04d.png")

    fps = metadata['fps']

    options = {}

    for key, value in metadata.items():
        if key in ["profile"]:
            options[f"-{key}:v"] = value
        elif key in ["level", "pix_fmt"]:
            options[f"-{key}"] = value

    options_str = ' '.join(f"{key} {value}" for key, value in options.items())

    try:
        ffmpeg_cmd.run("merge_frames", frames_pattern, str(fps), output, options_str)
        print(f"Successfully merged frames from {dir} into {output}")
    except RuntimeError as e:
        print(f"Error merging frames from {dir}: {e}")
    

def merge_streams(video_stream, audio_stream, output):
    if video_stream and audio_stream:
        try:
            ffmpeg_cmd.run("merge_streams", video_stream, audio_stream, output)
            print(f"Successfully merged streams into {output}")
        except RuntimeError as e:
            print(f"Error merging streams: {e}")
    else:
        print("Error: Missing video or audio stream path.")

def reconstruct(manifest, output):
    video_stream_path = None
    audio_stream_path = None

    for stream in manifest.streams.values():
        if stream["type"] == "video" and stream["status"] == "decomposed":
            stream_path = f"{os.path.dirname(stream['path'])}/stream_{stream['metadata']['index']}.mp4"
            merge_frames(stream["path"], stream["metadata"], stream_path)
            manifest.set_stream(stream["metadata"], stream_path, "composable")

            video_stream_path = stream_path
        elif stream["type"] == "audio":
            audio_stream_path = stream["path"]

    merge_streams(video_stream_path, audio_stream_path, output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reconstruct video files from manifest.")

    parser.add_argument("-m", "--manifest", type=str, required=True, help="Path to manifest file")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to output video file")

    args = parser.parse_args()

    manifest = video_tools.load_manifest(args.manifest)

    reconstruct(manifest, args.output)