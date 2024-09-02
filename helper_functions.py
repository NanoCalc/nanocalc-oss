import os
import uuid
import zipfile
import logging
from config import Config
from werkzeug.utils import secure_filename


"""
Save a file as a UUID-based name in the specified directory
and return its path
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
Generate a zip file with all the visible content from a source directory,
receive the targetDir and the webapp's name to construct the final URL.
Returns the zip file path inside this final URL.
"""
def generate_zip(sourceDir, webAppName, targetDir):
    zip_file_name = f"{uuid.uuid4()}-generated-data.zip"
    zip_file_path = os.path.join(targetDir, webAppName, zip_file_name)

    os.makedirs(os.path.join(targetDir, webAppName), exist_ok=True)

    with zipfile.ZipFile(zip_file_path, mode="w") as z:
        for filename in os.listdir(sourceDir): 
            file_path = os.path.join(sourceDir, filename)
            z.write(file_path, arcname=filename)

    return zip_file_path
    