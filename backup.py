from datetime import datetime, timedelta
import os
import shutil

# Configuration
CURRENT_WORKING_DIR = os.getcwd()
LOG_DIR = os.path.join(CURRENT_WORKING_DIR, "logs")
ARCHIVE_DIR = os.path.join(CURRENT_WORKING_DIR, "archive")
SOURCE_DIR = os.path.join(CURRENT_WORKING_DIR, "minecraft-data")
TARGET_DIR = os.path.join(CURRENT_WORKING_DIR, "backup")
BACKUP_RETENTION_TIME = 10
ARCHIVE_RETENTION_TIME = 30
LOG_RETENTION_TIME = 20

logfile_full_path = os.path.join(LOG_DIR, "Backup_log_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".log")
backupfolder_full_path = os.path.join(TARGET_DIR, "Backup_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))


def log_write(message):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_entry = f"[{timestamp}] {message}\n"
    # Write to log file
    with open(logfile_full_path, 'a') as log_file:
        log_file.write(log_entry)

def sorted_listing_by_creation_time(directory):
    def get_creation_time(item):
        item_path = os.path.join(directory, item)
        return os.path.getctime(item_path)

    items = os.listdir(directory)
    sorted_items = sorted(items, key=get_creation_time)
    return sorted_items

def get_old_files(directory, retention_days):
    today = datetime.now()
    retention_timestamp = (today - timedelta(days=retention_days)).timestamp()

    old_files = [] # List where we will store names of the old folders
    # Scan directory
    for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            
            creation_time = os.path.getctime(item_path)
            
            # Check if file was created yesterday
            if creation_time < retention_timestamp:
                old_files.append({
                    'name': item,
                })

    return old_files


def delete_old_logfiles():
    log_write(f"Log file deletion process started")

    old_files = get_old_files(LOG_DIR, LOG_RETENTION_TIME)

    for file in old_files:
        try: 
            os.remove(os.path.join(LOG_DIR, file))
            log_write(f"File {file} was removed from {LOG_DIR}")
        except Exception as e:
            log_write(f"File deletion failed with error {e}")

    log_write(f"Log file deletion process finished")

def delete_old_archivefiles():
    log_write(f"Archive file deletion process started")
    
    old_files = get_old_files(ARCHIVE_DIR, ARCHIVE_RETENTION_TIME)

    for file in old_files:
        try: 
            os.remove(os.path.join(ARCHIVE_DIR, file))
            log_write(f"File {file} was removed from {ARCHIVE_DIR}")
        except Exception as e:
            log_write(f"File deletion failed with error {e}")

    log_write(f"Archive file deletion process finished") 

def move_old_folders_to_archive():
    log_write(f"Move old folders to archive process started")
    
    old_folders = get_old_files(TARGET_DIR, BACKUP_RETENTION_TIME)

    for folder in old_folders:
        try: 
            os.remove(os.path.join(TARGET_DIR, folder))
            shutil.make_archive(folder, 'zip')
            shutil.move(os.path.join(TARGET_DIR, folder + ".zip"), ARCHIVE_DIR)
            log_write(f"Folder {folder} was removed from {TARGET_DIR}")
        except Exception as e:
            log_write(f"Folder deletion failed with error {e}")

    log_write(f"Move old folders to archive process finished") 


if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

log_write("===== Minecraft Backup Script Started =====")

if os.path.exists(SOURCE_DIR):
    log_write(f"Source directory {SOURCE_DIR} exists")

    if not os.path.exists(ARCHIVE_DIR):
        os.mkdir(ARCHIVE_DIR)
        log_write(f"Archive directory {ARCHIVE_DIR} was created")

    # Backup part
    log_write("Backup part started")

    if not os.path.exists(TARGET_DIR):
        os.mkdir(TARGET_DIR)
        log_write(f"Target directory {TARGET_DIR} was created")

    if not os.path.exists(backupfolder_full_path):
        os.mkdir(backupfolder_full_path)
        log_write(f"Folder for backup {backupfolder_full_path} was created")
    try:
        log_write("Backup started")

        shutil.copytree(SOURCE_DIR, backupfolder_full_path, dirs_exist_ok=True)

        log_write("Backup finished")
    except Exception as e:
        log_write(f"Error during backup: {e}")

    log_write("Backup part finished")

    # Cleaning part
    log_write("Cleaning part started")

    move_old_folders_to_archive()
    delete_old_logfiles()
    delete_old_archivefiles()

    log_write("Cleaning part finished")
    
else:
    log_write(f"Source directory {SOURCE_DIR} does not exist")


log_write("===== Minecraft Backup Script Finished =====")
