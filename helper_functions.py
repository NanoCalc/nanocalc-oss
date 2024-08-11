import os
import uuid
import zipfile
import logging
from config import Config
from functools import wraps
from flask import request


"""
Returns True if the file extension is in the list of allowed extensions
"""
def allowed_file(filename, ext):
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ext


"""
Save a file with a UUID-based name and return its path
"""
def save_file_with_uuid(directory, file, extension):
    if not os.path.exists(directory):
        logging.warning(f"Directory {directory} does not exist. Creating it.")
        os.makedirs(directory)

    filename = f"{uuid.uuid4()}.{extension}"
    filepath = os.path.join(directory, filename)
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
    return zip_file_name
