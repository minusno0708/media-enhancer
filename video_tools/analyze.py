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

def parse_video_metadata(stream_info):
    dict_metadata = {}

    for key, value in stream_info.items():
        dict_metadata[key] = value

    frame_rate_parts = stream_info.get('r_frame_rate', '0/1').split('/')
    if len(frame_rate_parts) == 2 and frame_rate_parts[1] != '':
        dict_metadata['fps'] = int(frame_rate_parts[0]) / int(frame_rate_parts[1])
    else:
        dict_metadata['fps'] = 0

    for key in ["index", "codec_name", "width", "height", "fps"]:
        if key not in dict_metadata:
            raise ValueError(f"Missing required video metadata key: {key}")
    return dict_metadata

def parse_audio_metadata(stream_info):
    dict_metadata = {}
    for key, value in stream_info.items():
        dict_metadata[key] = value

    for key in ["index", "codec_name"]:
        if key not in dict_metadata:
            raise ValueError(f"Missing required audio metadata key: {key}")
        
    return dict_metadata

def analyze(path):
    if not os.path.isfile(path):
        raise ValueError(f"The path {path} is not a valid file.")
    
    if not path.lower().endswith(('.mp4')):
        raise ValueError("The file is not an MP4 video.")

    try:
        result = ffmpeg_cmd.run("probe_video", path)
    except RuntimeError as e:
        print(f"Error retrieving video info: {e}")
        return
    
    parse_result = parse_ffprobe_output(result)
    
    streams = []

    for stream_info in parse_result:
        codec_type = stream_info.get('codec_type')
        if codec_type == 'video':
            streams.append(parse_video_metadata(stream_info))
        elif codec_type == 'audio':
            streams.append(parse_audio_metadata(stream_info))

    return streams

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze video files.")
    parser.add_argument("-path", type=str, help="Path to the video file")
    args = parser.parse_args()

    result = analyze(args.path)
    print(result)