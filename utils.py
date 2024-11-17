import os
import re
from datetime import datetime
import zipfile
import shutil 
import tempfile

def get_clean_file_name(file_name):
    if not file_name:
        return
    role = os.path.splitext(file_name)[0]
    role = [
        role_split
        for role_split in re.split("[^a-z]", role.lower())
        if role_split.strip()
    ]
    role.append(str(int(datetime.now().timestamp())))
    role = "_".join(role)
    return role

def process_zip_file(zip_content, output_folder):
    with tempfile.TemporaryDirectory() as tempdir:
        # Extract the zip file
        with zipfile.ZipFile(zip_content, "r") as zip_ref:
            zip_ref.extractall(tempdir)

        # Ensure output directory exists
        os.makedirs(output_folder, exist_ok=True)

        # Iterate over the files in the temporary directory
        for filename in os.listdir(tempdir):
            file_path = os.path.join(tempdir, filename)
            extension = os.path.splitext(filename)[1].lower()

            if extension == ".pdf":
                # Move PDF directly to the output folder
                save_path = os.path.join(output_folder, filename)
                shutil.move(file_path, save_path)
            elif extension == ".docx":
                # Move DOCX directly to the output folder
                save_path = os.path.join(output_folder, filename)
                shutil.move(file_path, save_path)
