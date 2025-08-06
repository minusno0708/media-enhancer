import os
import glob

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_children(path):
    return glob.glob(os.path.join(path, '*'))
