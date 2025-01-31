import os
import shutil
import zipfile
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

zip_file_path = config.get('Directory', 'zip_path')

def process_all_zip_files(directory_path, destination_dir):
    # Get a list of all files in the directory
    files = os.listdir(directory_path)

    # Filter out only the ZIP files
    zip_files = [file for file in files if file.lower().endswith('.zip')]

    # Process each ZIP file
    for zip_file in zip_files:
        zip_file_path = os.path.join(directory_path, zip_file)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            zip_file.extractall(destination_dir)
            os.remove(zip_file_path)

destination_dir = config.get('Directory', 'extract_path')
process_all_zip_files(zip_file_path, destination_dir)