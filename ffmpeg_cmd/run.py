import subprocess
import os

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts/')

def run(script, *args):
    script_path = SCRIPTS_DIR + script + '.sh'
    command = ['sh', script_path, ] + list(args)
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg command failed: {result.stderr}")
    return result.stdout