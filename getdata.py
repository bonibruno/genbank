# getdata.py
#
# Import required libraries
from ftplib import FTP
import os
import logging
import time

# Initialize logging to capture error messages in 'getdata.log'
logging.basicConfig(filename='getdata.log', level=logging.ERROR)

# Function to connect to the FTP server
def connect_ftp():
    ftp = FTP('ftp.ncbi.nlm.nih.gov')
    ftp.login('anonymous', 'password')
    return ftp

# Function to download directory from FTP server to local
def download_directory(remote_path, local_path, max_retries=3):
    # Loop to retry connecting to the FTP server in case of errors
    for retry_count in range(max_retries):
        try:
            ftp = connect_ftp()  # Re-initialize the FTP connection
            ftp.cwd(remote_path)  # Change to the remote directory
            break
        except Exception as e:
            logging.error(f"Failed to change directory to {remote_path} on try {retry_count + 1}: {str(e)}")
            ftp.quit()
            time.sleep(2)  # Wait before retrying
            continue
    else:
        logging.error(f"Max retries reached. Skipping {remote_path}")
        return

    # Create the local directory if it doesn't exist
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    # Loop through each file and directory in the remote directory
    for name, attr in ftp.mlsd(remote_path):
        remote_elem_path = f"{remote_path}/{name}"
        local_elem_path = os.path.join(local_path, name)

        # If it's a directory, call the function recursively
        if attr['type'] == 'dir':
            download_directory(remote_elem_path, local_elem_path)
        # If it's a file, download it
        elif attr['type'] == 'file':
            try:
                with open(local_elem_path, 'wb') as local_file:
                    ftp.retrbinary(f"RETR {remote_elem_path}", local_file.write)
                print(f"Downloaded {remote_elem_path} to {local_elem_path}...")
            except Exception as e:
                logging.error(f"Failed to download {remote_elem_path}: {str(e)}")
                ftp.quit()
                return
    ftp.quit()

# Main section of the script
if __name__ == '__main__':
    try:
        # List of directories to download
        directories_to_get = ['GDS1nnn', 'GDS2nnn', 'GDS3nnn', 'GDS4nnn', 'GDS5nnn', 'GDS6nnn', 'GDSnnn']

        # Loop through each directory and download it
        for dir_to_get in directories_to_get:
            try:
                remote_dir = f"/geo/datasets/{dir_to_get}"
                local_dir = os.path.join('geo_datasets', dir_to_get)
                download_directory(remote_dir, local_dir)
            except Exception as e:
                logging.error(f"Failed to download directory {remote_dir}: {str(e)}")
                continue

    except Exception as e:
        logging.error(f"Script failed: {str(e)}")
