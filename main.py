import argparse
import os
import shutil
import glob

import video_tools

VIDEO_EXTENSIONS = ("mp4",)
IMAGE_EXTENSIONS = ("jpg",)

WORKSPACE_DIR = "workspace"

def build_metadata(src_path, output_dir):
    result = {}

    result["src_path"] = src_path

    file_path = "/".join(src_path.split('/')[1:])
    result["dest_path"] = os.path.join(output_dir, file_path)

    result["workspace_dir"] = WORKSPACE_DIR + '/' + file_path.split('.')[0]
    print(result["workspace_dir"])

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
        dir_contents = glob.glob(os.path.join(file_metadata["src_path"], '*'))
    
        if not os.path.exists(file_metadata["dest_path"]):
            os.makedirs(file_metadata["dest_path"])

        for content_path in dir_contents:
            run(content_path, output_dir)

    elif file_metadata["type"] == 'video':
        video_tools.decompose(src_path, output_dir)
    elif file_metadata["type"] == 'image':
        # 仮の処理として画像ファイルをコピー
        shutil.copy(file_metadata['src_path'], file_metadata['dest_path'])
    else:
        print(f"{file_metadata['src_path']} is unsupported file type. Skipping.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video and image files.")
    parser.add_argument("-s", "--src", type=str, required=True, help="Source Path")
    parser.add_argument("-d", "--dest", type=str, required=True, help="Destination Path")

    args = parser.parse_args()
    
    run(args.src, args.dest)
