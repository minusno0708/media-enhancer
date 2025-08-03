import os
import sys

video_extensions = (".mp4")
image_extensions = (".jpg")

TYPE_KEY = "type"
EXT_KEY = "ext"

def categorize_path(input_path, output_path):
    result = {}

    result["input"] = input_path

    if os.path.isdir(input_path):
        result[TYPE_KEY] = 'folder'
        return result

    ext = input_path.split('.')[-1]
    result[EXT_KEY] = ext

    if ext in video_extensions:
        result[TYPE_KEY] = 'video'
    elif ext in image_extensions:
        result[TYPE_KEY] = 'image'
    else:
        result[TYPE_KEY] = 'unsupported'

    file_path = "/".join(input_path.split('/')[1:])
    result["output"] = os.path.join(output_path, file_path)

    return result

def get_folder_elements(folder_path):
    elements = []
    for root, _, files in os.walk(folder_path):
        for name in files:
            elements.append(os.path.join(root, name))
    return elements

def run(input_path, output_path):
    path_category = categorize_path(input_path, output_path)

    print(F"処理開始: {path_category['input']}")

    if path_category[TYPE_KEY] == 'folder':
        folder_elements = get_folder_elements(input_path)
        for element in folder_elements:
            run(element, output_path)
    elif path_category[TYPE_KEY] == 'video':
        print("動画ファイルの処理は未実装です")
    elif path_category[TYPE_KEY] == 'image':
        print("画像ファイルの処理は未実装です")
    else:
        print(f"{path_category['input']} はサポートされていないファイル形式です")

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <input_path> <output_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    run(input_path, output_path)

if __name__ == "__main__":
    main()
