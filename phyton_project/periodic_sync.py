# periodic_sync.py
import time
import logging
from datetime import datetime
from setup_logging import setup_logging
from sync_folders import sync_folders

def periodic_sync(source_folder, replica_folder, interval_seconds, log_file):
    setup_logging(log_file)  # Initialize logging
    while True:
        logging.info(f"Starting synchronization at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        sync_folders(source_folder, replica_folder)
        logging.info(f"Synchronization completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"Next sync in {interval_seconds} seconds...\n")
        time.sleep(interval_seconds)
