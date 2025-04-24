import os
import shutil
import time
import logging
import sys # Import sys to get the script's path



user_profile = os.path.expanduser("~") 
watch_folder = os.path.join(user_profile, "Downloads") # The folder to monitor

check_interval_seconds = 1800 # 30 minutes * 60 seconds/minute


script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
log_file = os.path.join(script_directory, 'sorter_log.txt')

# Define sorting rules: Category Name -> List of lowercase extensions
sorting_rules = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'],
    'Documents': ['.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls', '.txt', '.rtf', '.odt'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Installers': ['.exe', '.msi'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
    'Video': ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv'],
    # 'Other' is handled implicitly for non-matching files
}

# --- Logging Setup ---

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file,
    filemode='a'
)



# --- Sorting Function ---
def sort_downloads():
    """
    Checks the watch_folder for files and moves them to category subfolders.
    """
    logging.info(f"Checking folder: {watch_folder}")

    try:
        # List items in the directory
        items = os.listdir(watch_folder)
    except FileNotFoundError:
        logging.error(f"Watch folder not found: {watch_folder}")
        return
    except PermissionError:
        logging.error(f"Permission denied to access folder: {watch_folder}")
        return
    except Exception as e:
        logging.error(f"Error listing items in {watch_folder}: {e}")
        return

    for item_name in items:
        item_path = os.path.join(watch_folder, item_name)

        # Skip if it's a directory (prevents trying to move the category folders)
        if os.path.isdir(item_path):
            continue

        # Skip if it's the log file itself (unlikely to be in Downloads, but safe)
        if item_path == log_file:
             continue

        # Process only files
        if os.path.isfile(item_path):
            try:
                # Get file extension and convert to lowercase
                _, file_extension = os.path.splitext(item_name)
                file_extension = file_extension.lower()

                destination_subfolder_name = 'Other' # Default category

                # Find the correct category based on extension
                for category, extensions in sorting_rules.items():
                    if file_extension in extensions:
                        destination_subfolder_name = category
                        break 

                # Construct destination paths
                destination_folder_path = os.path.join(watch_folder, destination_subfolder_name)
                destination_file_path = os.path.join(destination_folder_path, item_name)

                # Create the destination folder if it doesn't exist
                os.makedirs(destination_folder_path, exist_ok=True) # exist_ok=True prevents error if folder exists

                # Move the file
                logging.info(f"Moving '{item_name}' to '{destination_subfolder_name}' folder.")
                shutil.move(item_path, destination_file_path)
                logging.info(f"Successfully moved '{item_name}'.")

            except PermissionError:
                logging.warning(f"Permission denied to move file: '{item_name}'. Skipping.")
            except FileNotFoundError:
                 # This can happen if the file is deleted between listing and processing
                 logging.warning(f"File not found (may have been moved or deleted): '{item_name}'. Skipping.")
            except shutil.Error as e:
                 logging.error(f"Shutil error moving file '{item_name}': {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred processing file '{item_name}': {e}")

# --- Main Execution Loop ---
if __name__ == "__main__":
    logging.info("Download Sorter script started.")
    while True:
        sort_downloads()
        logging.info(f"Check cycle complete. Waiting {check_interval_seconds} seconds...")
        time.sleep(check_interval_seconds)