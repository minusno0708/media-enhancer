import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import ffmpeg_cmd

def parse_ffprobe_output(output):
    stream_parts = output.strip().split('[/STREAM]')
    streams = []
    for part in stream_parts:
        stream_dict = {}
        for row in part.strip().splitlines():
            if row.startswith('[STREAM]') or not row.strip():
                continue
            key_value = row.split('=', 1)
            if len(key_value) == 2:
                key, value = key_value
                stream_dict[key.strip()] = value.strip()
        streams.append(stream_dict)
    return streams

def get_prove_diff(from_file, to_file):
    try:
        from_result = ffmpeg_cmd.run("probe_video", from_file)
        to_result = ffmpeg_cmd.run("probe_video", to_file)
    except RuntimeError as e:
        print(f"Error retrieving video info: {e}")
        return
    
    from_streams = parse_ffprobe_output(from_result)
    to_streams = parse_ffprobe_output(to_result)

    diff_result = {}

    for streams in from_streams:
        streams_index = streams.get("index")
        diff_result[streams_index] = {}
        for key, value in streams.items():
            diff_result[streams_index][key] = (value, None)

    for streams in to_streams:
        streams_index = streams.get("index")
        if streams_index not in diff_result:
            diff_result[streams_index] = {}
        for key, value in streams.items():
            if key in diff_result[streams_index]:
                diff_result[streams_index][key] = (diff_result[streams_index][key][0], value)
            else:
                diff_result[streams_index][key] = (None, value)

    for streams in diff_result:
        print(f"Stream {streams}:")
        for key, value in diff_result[streams].items():
            if value[0] != value[1]:
                print(f"  {key}: {value[0]} -> {value[1]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze video files.")
    parser.add_argument("-f", "--from_file", type=str, help="Path to the from video file")
    parser.add_argument("-t", "--to_file", type=str, help="Path to the to video file")
    args = parser.parse_args()

    result = get_prove_diff(args.from_file, args.to_file)
