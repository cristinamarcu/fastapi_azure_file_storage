import gzip
import shutil


def compress_file(file_path):            

    with open(file_path, 'rb') as f_in:
        with gzip.open(file_path + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    return f_out


def file_decompressed(file_path):
    try:
        with gzip.open(file_path + '.gz', 'rb') as f_in:
            content=f_in.read()
    except gzip.BadGzipFile:
        print("The file is not a valid Gzip file.")
        return None
        
    return content



