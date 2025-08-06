import os

def get_files_in_directory(path):
    file_paths = []
    for root, _, files in os.walk(path):
        for name in files:
            file_paths.append(os.path.join(root, name))
    return file_paths