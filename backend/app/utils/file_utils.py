import os
import hashlib
import shutil
import logging

def file_exists(file_path):
    return os.path.isfile(file_path)

def compute_file_hash(file):
    """Compute the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file.read(4096), b""):
        hash_md5.update(chunk)
    file.seek(0)  # Reset file pointer
    return hash_md5.hexdigest()

def clear_directory(directory_path):
    """
    Clears the specified directory by removing it and then recreating it.
    """
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        os.makedirs(directory_path)
        logging.info(f"Directory cleared: {directory_path}")