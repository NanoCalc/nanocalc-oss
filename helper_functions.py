import os
import uuid
import zipfile
import logging
from config import Config
from visitor import db, Visitor
from functools import wraps

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


def get_unique_sessions():
    """
    Return the number of unique sessions 
    """
    unique_sessions = db.session.query(Visitor.session_id).distinct().count()
    return unique_sessions


def log_vistor(f):
    """
    Decorator to log the amount of unique visitors to the website
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'Unknown')
        #operating_system = parse_os_from_user_agent(user_agent) 
        #country = get_country_from_ip(ip) 

        # Create a new visitor entry
        visitor = Visitor(ip, user_agent)
        db.session.add(visitor)
        db.session.commit()

        return f(*args, **kwargs)

    return wrapper
