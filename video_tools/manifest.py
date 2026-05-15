import os
import json

stream_types = ["video", "audio"]
available_status = ["composable", "decomposed"]

class Manifest:
    def __init__(self):
        self.streams = {}

    def get_stream(self, index):
        if index not in self.streams:
            raise ValueError(f"Stream with index {index} does not exist in the manifest.")

        return self.streams[index]

    def set_stream(self, stream, path, status):    
        if status not in available_status:
            raise ValueError(f"Invalid status: {status}. Must be one of {available_status}")

        self.streams[stream["index"]] = {
            "type": stream["codec_type"],
            "path": path,
            "status": status,
            "metadata": stream
        }

    def save(self, directory, filename="manifest.json"):
        if not os.path.exists(directory):
            os.makedirs(directory)
        manifest_path = os.path.join(directory, filename)

        save_data = json.dumps({"streams": self.streams}, indent=4)

        with open(manifest_path, 'w') as f:
            f.write(save_data)

def load(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Manifest file not found at {path}")

    with open(path, 'r') as f:
        data = json.load(f)

    manifest = Manifest()
    for _, stream in data["streams"].items():
        manifest.set_stream(stream["metadata"], stream["path"], stream["status"])

    return manifest
