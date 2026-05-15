import argparse
import os
import shutil
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import video_tools
import video_tools.analyze as analyze
import ffmpeg_cmd

def extract_streams(filepath, output, streams):
    stream_files = {}

    for stream in streams:
        index = stream.get('index')

        if stream.get('codec_type') == 'video':
            output_path = f"{output}/stream_{index}.mp4"
        elif stream.get('codec_type') == 'audio':
            output_path = f"{output}/stream_{index}.m4a"

        try:
            ffmpeg_cmd.run("extract_stream", filepath, index, output_path)
            stream_files[index] = output_path
            print(f"Successfully extracted stream {index} to {output_path}")
        except RuntimeError as e:
            print(f"Error extracting stream {index}: {e}")
    print("Successfully extracted all streams.")

    return stream_files

def extract_frames(filepath, output):
    if not os.path.exists(output):
        os.makedirs(output)

    try:
        ffmpeg_cmd.run("extract_frames", filepath, output)
        print(f"Successfully extracted frames from {filepath} to {output}")
    except RuntimeError as e:
        print(f"Error extracting frames from {filepath}: {e}")

def decompose(filepath, output):
    streams = analyze(filepath)
    manifest = video_tools.Manifest()

    if not os.path.exists(output):
        os.makedirs(output)
    
    stream_files = extract_streams(filepath, output, streams)
    
    for stream in streams:
        index = stream["index"]
        codec_type = stream["codec_type"]

        manifest.set_stream(stream, stream_files[index], "composable")

        if codec_type == 'video':
            frame_path = f"{output}/frames_{index}"
            extract_frames(stream_files[index], frame_path)
            os.remove(stream_files[index])
            manifest.set_stream(stream, frame_path, "decomposed")

    manifest.save(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decompose streams from a video file.")
    parser.add_argument("-f", "--file", type=str, required=True, help="Input Path")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output Path")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output directory")

    args = parser.parse_args()

    if args.overwrite and os.path.exists(args.output):
        shutil.rmtree(args.output)
    
    decompose(args.file, args.output)