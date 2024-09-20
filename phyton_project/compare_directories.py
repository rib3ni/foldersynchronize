# compare_directories.py
import os
import shutil
import logging
from filecmp import dircmp

def compare_directories(source_dir, replica_dir):
    comparison = dircmp(source_dir, replica_dir)

    # Remove files from replica if they don't exist in source
    for file_name in comparison.right_only:
        full_path = os.path.join(replica_dir, file_name)
        if os.path.isfile(full_path):
            os.remove(full_path)
            logging.info(f"Removed: {full_path}")
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)
            logging.info(f"Removed directory: {full_path}")

    # Recursively check subdirectories
    for common_dir in comparison.common_dirs:
        compare_directories(os.path.join(source_dir, common_dir), os.path.join(replica_dir, common_dir))
