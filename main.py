import argparse
import os
import shutil

from utils import directory_utils
from video_tools import analyzer

VIDEO_EXTENSIONS = (".mp4")
IMAGE_EXTENSIONS = (".jpg")

def build_metadata(src_path, output_dir):
    result = {}

    result["src_path"] = src_path

    file_path = "/".join(src_path.split('/')[1:])
    result["dest_path"] = os.path.join(output_dir, file_path)

    if os.path.isdir(src_path):
        result["type"] = 'directory'
        return result

    ext = src_path.split('.')[-1]
    result["extension"] = ext

    if ext in VIDEO_EXTENSIONS:
        result["type"] = 'video'
    elif ext in IMAGE_EXTENSIONS:
        result["type"] = 'image'
    else:
        result["type"] = 'unsupported'

    return result

def run(src_path, output_dir):
    file_metadata = build_metadata(src_path, output_dir)

    print(F"Processing: {file_metadata['src_path']}")

    if file_metadata["type"] == 'directory':
        dir_contents = directory_utils.get_children(file_metadata["src_path"])

        directory_utils.create_directory_if_not_exists(file_metadata["dest_path"])

        for content_path in dir_contents:
            run(content_path, output_dir)

    elif file_metadata["type"] == 'video':
        # 仮の処理として動画ファイルをコピー
        shutil.copy(file_metadata['src_path'], file_metadata['dest_path'])

        streams_metadata = analyzer.analyze(file_metadata['src_path'])
        print(f"Extracted metadata: {streams_metadata}")
    elif file_metadata["type"] == 'image':
        # 仮の処理として画像ファイルをコピー
        shutil.copy(file_metadata['src_path'], file_metadata['dest_path'])
    else:
        print(f"{file_metadata['src_path']} is unsupported file type. Skipping.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video and image files.")
    parser.add_argument("-src", "--source", type=str, required=True, help="Input Path")
    parser.add_argument("-dest", "--destination", type=str, required=True, help="Output Path")

    args = parser.parse_args()
    
    run(args.source, args.destination)
