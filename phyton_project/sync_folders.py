# sync_folders.py
import os
import shutil
import logging
from compare_directories import compare_directories

def sync_folders(source_dir, replica_dir):
    # Synchronize files from source to replica
    if not os.path.exists(replica_dir):
        os.makedirs(replica_dir)
        logging.info(f"Created directory: {replica_dir}")

    # Synchronize from source to replica
    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        replica_root = os.path.join(replica_dir, relative_path)

        # Create directories that exist in source but not in replica
        for dir_name in dirs:
            replica_subdir = os.path.join(replica_root, dir_name)
            if not os.path.exists(replica_subdir):
                os.makedirs(replica_subdir)
                logging.info(f"Created directory: {replica_subdir}")

        # Copy new or modified files to replica
        for file_name in files:
            source_file = os.path.join(root, file_name)
            replica_file = os.path.join(replica_root, file_name)
            if not os.path.exists(replica_file) or os.path.getmtime(source_file) > os.path.getmtime(replica_file):
                shutil.copy2(source_file, replica_file)
                logging.info(f"Copied: {source_file} -> {replica_file}")

    # Remove files and directories that exist in replica but not in source
    compare_directories(source_dir, replica_dir)
