import os
from math import floor
import io

MAX_FILE_SIZE = 20480000



def write_data_to_file(content, file_path):
    try:
        with open(file_path, "x") as f:
            f.write(str(content))
        return True
    except FileExistsError:
        return False


def get_file_size(file_path):
    try:
        file_size = os.path.getsize(file_path)
        # Convert size to kilobytes (KB)
        file_size_kb = file_size / 1024
        return file_size_kb

    except OSError as e:
        print(f"Error: {e}")
        return None


def validate_file_size(file_path):
    file_size = get_file_size(file_path)

    if file_size > MAX_FILE_SIZE:
        return False
    else:
        return True
