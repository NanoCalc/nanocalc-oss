from fretcalc_core import overlap_calculation
from ricalc_core import n_calculation, n_k_calculation
from plqsim_facade import execute_plqsim_operation, PlqSimOperation
from tmmsim_core import calculation
import os 
import logging
from waitress import serve
from flask import Flask, request, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from apps_definitions import allowed_extensions, get_max_files, get_allowed_extensions
from helper_functions import save_file_with_uuid, generate_zip
from config import Config
from shutil import rmtree

# App configuration
app = Flask(__name__)
app.config.from_object(Config)

# Logging configuration
log_file_path = os.path.join(Config.LOG_PATH, 'backend.log')
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# Create a custom logger
logger = logging.getLogger()
logger.setLevel(Config.LOGGING_LEVEL)

# Create handlers
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(Config.LOGGING_LEVEL)

console_handler = logging.StreamHandler()
console_handler.setLevel(Config.LOGGING_LEVEL)

# Create formatter and add it to handlers
formatter = logging.Formatter(Config.LOGGING_FORMAT)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

#TODO: create unique folders?
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

FILE_ID_FORM_FIELD = 'NANOCALC_FILE_ID_FORM_FIELD'
FILES_FORM_FIELD = 'NANOCALC_USER_UPLOADED_FILES'
MODE_FORM_FIELD = 'NANOCALC_USER_MODE'


def respond_client(message, code):
    return jsonify({
        'message': message
    }), code


def handle_fretcalc(files_bundle):
    fretcalc_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'fretcalc')
    input_excel_path = None
    extinction_coefficient_path = None
    emission_coefficient_path = None
    refractive_index_path = None 
    dataFolderPath = None

    try:
        input_excel_path = save_file_with_uuid(fretcalc_folder, files_bundle['inputExcel'])
        extinction_coefficient_path = save_file_with_uuid(fretcalc_folder, files_bundle['extinctionCoefficient'])
        emission_coefficient_path = save_file_with_uuid(fretcalc_folder, files_bundle['emissionCoefficient'])
        refractive_index_path = save_file_with_uuid(fretcalc_folder, files_bundle['refractiveIndex'])

        dataFolderPath = overlap_calculation(input_excel_path, extinction_coefficient_path, emission_coefficient_path, refractive_index_path, UPLOAD_FOLDER)
        zip_file_name = generate_zip(dataFolderPath, 'fretcalc', app.config['UPLOAD_FOLDER'])
        return zip_file_name

    except Exception as e: 
        logging.error(f"handle_fretcalc.error: {e}")
        raise e
    finally:
        if input_excel_path and os.path.exists(input_excel_path):
            os.remove(input_excel_path)
        if extinction_coefficient_path and os.path.exists(extinction_coefficient_path):
            os.remove(extinction_coefficient_path)
        if emission_coefficient_path and os.path.exists(emission_coefficient_path):
            os.remove(emission_coefficient_path)
        if refractive_index_path and os.path.exists(refractive_index_path):
            os.remove(refractive_index_path)
        if dataFolderPath and os.path.exists(dataFolderPath):
            rmtree(dataFolderPath, ignore_errors=True)


def handle_ricalc(files_bundle):
    ricalc_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'ricalc')
    input_excel_path = None
    coefficient_path = None
    dataFolderPath = None

    try:
        input_excel_path = save_file_with_uuid(ricalc_folder, files_bundle['inputExcel'])
        mode = files_bundle['mode']

        if mode == 'opticalConstants':
            # calculate nk
            coefficient_path = save_file_with_uuid(ricalc_folder, files_bundle['decadicCoefficient'])
            dataFolderPath = n_k_calculation(input_excel_path, coefficient_path, None, UPLOAD_FOLDER)
        elif mode == 'refractiveIndex':
            # calculate n
            coefficient_path = save_file_with_uuid(ricalc_folder, files_bundle['constantK'])
            dataFolderPath = n_calculation(input_excel_path, coefficient_path, None, UPLOAD_FOLDER)
        else:
            #TODO: throw?
            pass
        
        zip_file_name = generate_zip(dataFolderPath, 'ricalc', app.config['UPLOAD_FOLDER'])
        return zip_file_name
    except Exception as e: 
        logging.error(f"handle_ricalc.error: {e}")
        raise e
    finally:
        if input_excel_path and os.path.exists(input_excel_path):
            os.remove(input_excel_path)
        if coefficient_path and os.path.exists(coefficient_path):
            os.remove(coefficient_path)
        if dataFolderPath and os.path.exists(dataFolderPath):
            rmtree(dataFolderPath, ignore_errors=True)


def handle_plqsim(files_bundle):
    plqsim_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'plqsim')
    input_excel_path = None
    dataFolderPath = None

    try:
        input_excel_path = save_file_with_uuid(plqsim_folder, files_bundle['inputExcel'])
        mode = files_bundle['mode']
        execute_plqsim_operation(PlqSimOperation.ENERGY_LEVEL, input_excel_path, None, UPLOAD_FOLDER)

        if mode == 'donorExcitation':
            dataFolderPath = execute_plqsim_operation(PlqSimOperation.DONOR_EXCITATION, input_excel_path, None, UPLOAD_FOLDER)
        elif mode == 'acceptorExcitation':
            dataFolderPath = execute_plqsim_operation(PlqSimOperation.ACCEPTOR_EXCITATION, input_excel_path, None, UPLOAD_FOLDER)
        else:
            #TODO: throw?
            pass
        
        zip_file_name = generate_zip(dataFolderPath, 'plqsim', app.config['UPLOAD_FOLDER'])
        return zip_file_name
    except Exception as e:
        logging.error(f"handle_plqsim.error: {e}")
        raise e
    finally:
        if input_excel_path and os.path.exists(input_excel_path):
            os.remove(input_excel_path)
        if dataFolderPath and os.path.exists(dataFolderPath):
            rmtree(dataFolderPath, ignore_errors=True)


def handle_tmmsim(files_bundle):
    tmmsim_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'tmmsim')
    input_excel_path = None
    dataFolderPath = None
    csv_paths = []
    
    try:
        input_excel_path = save_file_with_uuid(tmmsim_folder, files_bundle['inputExcel'])

        layerFiles = [layerFile for layerFile in files_bundle.get('layerFiles', []) if layerFile]
        for layerFile in layerFiles:
            csv_path = os.path.join(tmmsim_folder, secure_filename(layerFile.filename))
            layerFile.save(csv_path)
            csv_paths.append(csv_path)

        dataFolderPath = calculation(tmmsim_folder, input_excel_path, UPLOAD_FOLDER, None)
        zip_file_name = generate_zip(dataFolderPath, 'tmmsim', app.config['UPLOAD_FOLDER'])
        return zip_file_name

    except Exception as e:
        logging.error(f"handle_tmmsim.error: {e}")
        raise e
    finally:
        if input_excel_path and os.path.exists(input_excel_path):
            os.remove(input_excel_path)
        if dataFolderPath and os.path.exists(dataFolderPath):
            rmtree(dataFolderPath, ignore_errors=True)
        for csv_path in csv_paths:
            if csv_path and os.path.exists(csv_path):
                os.remove(csv_path)
       

app_handlers = {
    'fretcalc': handle_fretcalc,
    'ricalc': handle_ricalc,
    'plqsim': handle_plqsim,
    'tmmsim': handle_tmmsim,
}


@app.route('/health', methods=['GET'])
def health():
    return respond_client('Up and running!', 200)

#TODO: implement queueing system
@app.route('/upload/<app_name>', methods=['POST'])
def upload_file(app_name):
    try:
        requestFiles = request.files
        requestForm = request.form
        
        if FILES_FORM_FIELD not in requestFiles or FILE_ID_FORM_FIELD not in requestForm:
            return respond_client('emptyOrUnidentifiedRequest', 400)

        files = [file for file in requestFiles.getlist(FILES_FORM_FIELD) if file.filename]
        file_ids = requestForm.getlist(FILE_ID_FORM_FIELD)

        if len(file_ids) != len(files):
            return respond_client('mismatchedFileIdsAndFiles', 400)
        
        amountUploadedFiles = len(files)
        maxAllowedUploadedFiles = get_max_files(app_name)
        
        if amountUploadedFiles > maxAllowedUploadedFiles:
            logging.error(f"uploadFileError.tooManyFiles: client uploaded {amountUploadedFiles}. Max allowed is: {maxAllowedUploadedFiles}")
            return respond_client('tooManyFiles', 413)

        allowed_extensions = get_allowed_extensions(app_name)

        for file in files:
            if file.filename.split(".").pop() not in allowed_extensions:
                logging.error(f"uploadFileError.badExtension: client uploaded {file.filename}. Extension not allowed.")
                return respond_client('badExtension', 400)


        files_bundle = {}
        mode = requestForm.get(MODE_FORM_FIELD)
        if mode:
            files_bundle['mode'] = mode
        
        for file_id, file in zip(file_ids, files):
            if file_id == 'layerFiles':
                if file_id not in files_bundle:
                    files_bundle[file_id] = []
                files_bundle[file_id].append(file)
            else:
                files_bundle[file_id] = file

        
        zip_file_path = app_handlers[app_name](files_bundle)
        
        try:
            directory = os.path.dirname(zip_file_path)
            filename = os.path.basename(zip_file_path)

            return send_from_directory(directory=directory, path=filename, as_attachment=True)
        except Exception as e:
            logging.error(f"Error in sending file: {e}")
            return respond_client('Failed to send zip file', 500)
        finally:
            if zip_file_path and os.path.exists(zip_file_path):
                os.remove(zip_file_path)


    except RequestEntityTooLarge as e:
        return respond_client('tooLargeRequest', 413)
    except Exception as e:
        logging.exception(f"uploadFileError.genericError")
        return respond_client('internalServerError', 500)


if __name__ == "__main__":
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 8080)) 

    if debug_mode:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=True,
        )
    else:
        serve(app, threads=100)
