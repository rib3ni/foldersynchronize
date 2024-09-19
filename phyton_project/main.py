import os
import shutil
from filecmp import dircmp
from datetime import datetime
import time
import logging

# Configure logging to both file and console
def setup_logging(log_file):
    # Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()

    # Set the logging level for both handlers
    file_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

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

def periodic_sync(source_folder, replica_folder, interval_seconds, log_file):
    setup_logging(log_file)  # Initialize logging
    while True:
        logging.info(f"Starting synchronization at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        sync_folders(source_folder, replica_folder)
        logging.info(f"Synchronization completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"Next sync in {interval_seconds} seconds...\n")
        time.sleep(interval_seconds)

# Run synchronization periodically
if __name__ == "__main__":
    # Ask the user for input
    source_folder = input("Enter the source folder path: ")
    replica_folder = input("Enter the replica folder path: ")
    interval_seconds = int(input("Enter the interval time in seconds: "))
    log_file = input("Enter the log file path (e.g., sync_log.txt): ")

    periodic_sync(source_folder, replica_folder, interval_seconds, log_file)
