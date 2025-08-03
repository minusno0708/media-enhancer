import os
import sys

VIDEO_EXTENSIONS = (".mp4")
IMAGE_EXTENSIONS = (".jpg")

def build_metadata(input_path, output_path):
    result = {}

    result["input_path"] = input_path

    if os.path.isdir(input_path):
        result["type"] = 'directory'
        return result

    ext = input_path.split('.')[-1]
    result["extension"] = ext

    if ext in VIDEO_EXTENSIONS:
        result["type"] = 'video'
    elif ext in IMAGE_EXTENSIONS:
        result["type"] = 'image'
    else:
        result["type"] = 'unsupported'

    file_path = "/".join(input_path.split('/')[1:])
    result["output_path"] = os.path.join(output_path, file_path)

    return result

def get_dir_contents(folder_path):
    contents = []
    for root, _, files in os.walk(folder_path):
        for name in files:
            contents.append(os.path.join(root, name))
    return contents

def run(input_path, output_path):
    file_metadata = build_metadata(input_path, output_path)

    print(F"処理開始: {file_metadata['input_path']}")

    if file_metadata["type"] == 'directory':
        dir_contents = get_dir_contents(file_metadata["input_path"])

        for content_path in dir_contents:
            run(content_path, output_path)

    elif file_metadata["type"] == 'video':
        print("動画ファイルの処理は未実装です")
    elif file_metadata["type"] == 'image':
        print("画像ファイルの処理は未実装です")
    else:
        print(f"{file_metadata['input_path']} はサポートされていないファイル形式です")

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <input_path> <output_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    run(input_path, output_path)

if __name__ == "__main__":
    main()
