import os
import uuid
import zipfile
import logging
from config import Config
from werkzeug.utils import secure_filename


"""
Save a file with a UUID-based name and return its path
"""
def save_file_with_uuid(directory, file):
    secure_name = secure_filename(file.filename)
    
    extension = os.path.splitext(secure_name)[1]
    new_filename = str(uuid.uuid4()) + extension
    
    os.makedirs(directory, exist_ok=True)
    
    filepath = os.path.join(directory, new_filename)
    file.save(filepath)
    return filepath


"""
Generate a zip file from a directory and return its name
"""
def generate_zip(path, webapp, upload_folder):
    zip_file_name = f"{uuid.uuid4()}-generated-data.zip"
    zip_file_path = os.path.join(upload_folder, webapp, zip_file_name)

    with zipfile.ZipFile(zip_file_path, mode="w") as z:
        for filename in os.listdir(path): 
            file_path = os.path.join(path, filename)
            z.write(file_path, arcname=filename)

    return zip_file_path
    