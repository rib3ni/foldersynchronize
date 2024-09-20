# main.py
import os
from periodic_sync import periodic_sync

def get_valid_folder_path(prompt_message):
    while True:
        folder_path = input(prompt_message)
        if os.path.isdir(folder_path):
            return folder_path
        else:
            print(f"Error: '{folder_path}' is not a valid directory. Please try again.")

if __name__ == "__main__":
    # Get valid source folder path
    source_folder = get_valid_folder_path("Enter the source folder path: ")

    # Get valid replica folder path
    replica_folder = get_valid_folder_path("Enter the replica folder path: ")

    # Validate the interval time input
    while True:
        try:
            interval_seconds = int(input("Enter the interval time in seconds: "))
            if interval_seconds > 0:
                break
            else:
                print("Error: Interval time must be a positive number.")
        except ValueError:
            print("Error: Please enter a valid number for the interval.")

    log_file = input("Enter the log file path (e.g., sync_log.txt): ")

    periodic_sync(source_folder, replica_folder, interval_seconds, log_file)
