import sys
import os

from utils import directory_utils

VIDEO_EXTENSIONS = (".mp4")
IMAGE_EXTENSIONS = (".jpg")

def build_metadata(src_path, dest_path):
    result = {}

    result["src_path"] = src_path

    file_path = "/".join(src_path.split('/')[1:])
    result["dest_path"] = os.path.join(dest_path, file_path)

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

def run(src_path, dest_path):
    file_metadata = build_metadata(src_path, dest_path)

    print(F"処理開始: {file_metadata['src_path']}")
    print(F"ディレクトリ内のファイル: {file_metadata}")

    if file_metadata["type"] == 'directory':
        dir_contents = directory_utils.get_children(file_metadata["src_path"])

        directory_utils.create_directory_if_not_exists(file_metadata["dest_path"])

        for content_path in dir_contents:
            run(content_path, dest_path)

    elif file_metadata["type"] == 'video':
        print("動画ファイルの処理は未実装です")
    elif file_metadata["type"] == 'image':
        print("画像ファイルの処理は未実装です")
    else:
        print(f"{file_metadata['src_path']} はサポートされていないファイル形式です")

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <source_path> <destination_path>")
        sys.exit(1)

    src_path = sys.argv[1]
    dest_path = sys.argv[2]

    run(src_path, dest_path)

if __name__ == "__main__":
    main()
