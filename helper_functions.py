import os
import uuid
import zipfile
import logging
from config import Config

def allowed_file(filename, ext):
    """
    Returns True if the file extension is in the list of allowed extensions
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ext


def save_file_with_uuid(directory, file, extension):
    """
    Save a file with a UUID-based name and return its path
    """
    if not os.path.exists(directory):
        logging.warning(f"Directory {directory} does not exist. Creating it.")
        os.makedirs(directory)

    filename = f"{uuid.uuid4()}.{extension}"
    filepath = os.path.join(directory, filename)
    file.save(filepath)
    return filepath
    

def generate_zip(path, webapp):
    """
    Generate a zip file from a directory and return its name
    """
    zip_file_name = f"{uuid.uuid4()}-generated-data.zip"
    zip_file_path = os.path.join(Config.UPLOAD_FOLDER, webapp, zip_file_name)
    with zipfile.ZipFile(zip_file_path, mode="w") as z:
        for filename in os.listdir(path): 
            file_path = os.path.join(path, filename)
            z.write(file_path, arcname=filename)
    return zip_file_name


# TODO: get number of sessions from database
def get_unique_sessions():
    """
    Return the number of unique sessions 
    """
    ips_path = os.path.join(app.root_path,'visitors.txt') 
    with open(ips_path, 'r') as file:
        ip_addresses = file.read().splitlines()

    unique_ip_count = len(ip_addresses)
    return unique_ip_count


# TODO: implement decorator here - be aware of context issues
# def log_vistor(f):
#     """Decorator to log the amount of unique visitors to the website"""
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         ip = request.remote_addr
#         ips_path = os.path.join(app.root_path,'visitors.txt')
#         with open(ips_path, 'a+') as file:
#             if ip not in file.read():
#                 file.write(ip + '\n')
#         return f(*args, **kwargs)
#     return wrapper