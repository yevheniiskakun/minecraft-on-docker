from datetime import datetime

LOG_DIR = "./logs"

SOURCE_DIR = "./minecraft-data"
TARGET_DIR = "./backup"

logfile_full_path = LOG_DIR + "/" + "Backup_log_" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "_.log"

def create_dir(dir):
    pass

def create_file(file_path):
    pass

def log_write(log_path, message):
    pass



if os.path.exists(logfile_full_path):
    pass
else:
    pass
