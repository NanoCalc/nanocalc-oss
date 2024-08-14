from fret_calc import overlap_calculation
from ri_calc import n_calculation, n_k_calculation
from plq_sim import energy_level, donor_excitation, acceptor_excitation
from tmm_sim import calculation
import os 
import logging
from flask_caching import Cache
from waitress import serve
from flask import Flask, request, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from apps_definitions import allowed_extensions, get_max_files, get_allowed_extensions
from helper_functions import save_file_with_uuid, generate_zip
from config import Config


# App configuration
app = Flask(__name__)
app.config.from_object(Config)
logging.basicConfig(level=Config.LOGGING_LEVEL, format=Config.LOGGING_FORMAT)
cache = Cache(app)
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
FORM_FIELD = 'NANOCALC_USER_UPLOADED_FILES'


def respond_client(message, code):
    return jsonify({
        'message': message
    }), code


# Client side caching
@app.after_request
def set_cache_headers(response):
    response.headers['Cache-Control'] = 'public, max-age=86400' 
    return response


def handle_fretcalc(files_bundle):
    fretcalc_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'fretcalc')
    
    try:
        input_excel_path = save_file_with_uuid(fretcalc_folder, files_bundle['inputExcel'])
        extinction_coefficient_path = save_file_with_uuid(fretcalc_folder, files_bundle['extinctionCoefficient'])
        emission_coefficient_path = save_file_with_uuid(fretcalc_folder, files_bundle['emissionCoefficient'])
        refractive_index_path = save_file_with_uuid(fretcalc_folder, files_bundle['refractiveIndex'])

        data = overlap_calculation(input_excel_path, extinction_coefficient_path, emission_coefficient_path, refractive_index_path, UPLOAD_FOLDER)
        zip_file_name = generate_zip(data, 'fretcalc', app.config['UPLOAD_FOLDER'])
        return zip_file_name

    except Exception as e: 
        logging.error(f"handle_fretcalc.error: {e}")
        raise e


def handle_ricalc(files_bundle):
    pass
def handle_plqsim(files_bundle):
    pass
def handle_tmmsim(files_bundle):
    pass


app_handlers = {
    'fretcalc': handle_fretcalc,
    'ricalc': handle_ricalc,
    'plqsim': handle_plqsim,
    'tmmsim': handle_tmmsim,
}

# RI Calculator - data upload
@app.route('/ricalc/submit', methods=['POST'])
def ri_calc_submit():
    appName = "RI-Calc"
    webApp = "ricalc"
    filesList = []

    try:
        if not request.files.getlist("kf"):
            files = request.files.getlist("xif")
            for file in files:
                if allowed_file(file.filename,['xlsx']):
                    xif = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'ri', 'index_files'), file, 'xlsx')
                    filesList.append(xif)
                else:
                    upload_error = UploadError("file_type", "index file", "xlsx", "ricalc")
                    return render_template("input_error.html", data=upload_error.to_dict())

            files = request.files.getlist("dacf")
            for file in files:
                if allowed_file(file.filename,['dat']):
                    dacf = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'ri', 'abs_coefficient_files'), file, 'dat')
                    filesList.append(dacf)
                else:
                    upload_error = UploadError("file_type", "absorption coefficient file", "dat", "ricalc")
                    return render_template("input_error.html", data=upload_error.to_dict())

            data_n_k = n_k_calculation(filesList[0], filesList[1], UPLOAD_FOLDER)
            zip_file_name = generate_zip(data_n_k, webApp, Config.UPLOAD_FOLDER)
            return render_template("upload_success.html", zip_name=zip_file_name,  app_name=appName, webapp=webApp)    

        elif not request.files.getlist("dacf"):
            files = request.files.getlist("xif")
            for file in files:
                if allowed_file(file.filename,['xlsx']):
                    xif = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'ri', 'index_files'), file, 'xlsx')
                    filesList.append(xif)
                else:
                    upload_error = UploadError("file_type", "index file", "xlsx", "ricalc")
                    return render_template("input_error.html", data=upload_error.to_dict())

            files = request.files.getlist("kf")
            for file in files:
                if allowed_file(file.filename,['dat']):
                    kf = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'ri', 'k_files'), file, 'dat')
                    filesList.append(kf)
                else:
                    upload_error = UploadError("file_type", "K file", "dat", "ricalc")
                    return render_template("input_error.html", data=upload_error.to_dict())

            data_n = n_calculation(filesList[0], filesList[1], UPLOAD_FOLDER)
            zip_file_name = generate_zip(data_n, webApp, Config.UPLOAD_FOLDER) 
            return render_template("upload_success.html", zip_name=zip_file_name,  app_name=appName, webapp=webApp) 
    except Exception as e:
        logging.warning(f"Error in RI-Calc: {e}")
        upload_error = UploadError("file_misformat", None, None, "ricalc")
        return render_template("input_error.html", data=upload_error.to_dict())


# PLQSim view - data upload
@app.route('/plqsim/submit', methods=['POST'])
def plq_sim_submit():
    appName = "PLQSim"
    webApp = "plqsim"
    try:
        index_file = request.files.getlist("xif")
        for file in index_file:
            if allowed_file(file.filename,['xlsx']):
                xif = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'plqsim', 'input_files'), file, 'xlsx')
            else:
                upload_error = UploadError("file_type", "index file", "xlsx", "plqsim")
                return render_template("input_error.html", data=upload_error.to_dict())

        energy_level(xif, UPLOAD_FOLDER) # Generate Energy Level plot for both choices
        action = request.form.get('action')

        if action == 'Calculate Acceptor Excitation':
            data = acceptor_excitation(xif, UPLOAD_FOLDER)
            zip_file_name = generate_zip(data, webApp, Config.UPLOAD_FOLDER)

        elif action == 'Calculate Donor Excitation':
            data = donor_excitation(xif,UPLOAD_FOLDER)
            zip_file_name = generate_zip(data,webApp, Config.UPLOAD_FOLDER)

        return render_template("upload_success.html", zip_name=zip_file_name,  app_name=appName, webapp=webApp)

    except Exception as e:
        logging.warning(f"Error in PLQSim: {e}")
        upload_error = UploadError("file_misformat", None, None, "plqsim")
        return render_template("input_error.html", data=upload_error.to_dict())


# TMMSim view - data upload
@app.route('/tmmsim/submit', methods=['POST'])
def tmm_sim_submit():
    appName = "TMMSim"
    webApp = "tmmsim"
    
    try:
        xif = request.files["xif"]

        if xif and allowed_file(xif.filename, ['xlsx']):
            xif = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'tmmsim' ,'input_files'), xif, 'xlsx')
        else:
            upload_error = UploadError("file_type", "index file", "xlsx", "tmmsim")
            return render_template("input_error.html", data=upload_error.to_dict())

        layer_files = request.files.getlist("layer_files")
        if len(layer_files) > 10:
            upload_error = UploadError(error_type="file_count", redirect_url="tmmsim", file_name=None, expected_ext=None)
            return render_template("input_error.html", data=upload_error.to_dict())

        csv_paths = []
        for file in layer_files:
            if allowed_file(file.filename, ['csv']):
                csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'tmmsim' ,'input_files', secure_filename(file.filename))
                file.save(csv_path)
                csv_paths.append(csv_path)
            else:
                upload_error = UploadError("file_type", "layer file", "csv", "tmmsim")
                return render_template("input_error.html", data=upload_error.to_dict())

        input_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'tmmsim' ,'input_files')
        data = calculation(xif, UPLOAD_FOLDER, input_dir)
        zip_file_name = generate_zip(data, webApp, Config.UPLOAD_FOLDER)
        return render_template("upload_success.html", zip_name=zip_file_name, app_name=appName, webapp=webApp)
    
    except Exception as e:
        logging.warning(f"Error in TMMSim: {e}")
        upload_error = UploadError("file_misformat", None, None, "tmmsim")
        return render_template("input_error.html", data=upload_error.to_dict())

@app.route('/upload/<app_name>', methods=['POST'])
def upload_file(app_name):
    try:
        requestFiles = request.files
        identifiers = request.form.getlist(f"{FORM_FIELD}_buttonId")

        if FORM_FIELD not in requestFiles or not identifiers:
            return respond_client('emptyOrUnidentifiedRequest', 400)

        files = [file for file in requestFiles.getlist(FORM_FIELD) if file.filename]
        
        amountUploadedFiles = len(files)
        maxAllowedUploadedFiles = get_max_files(app_name)

        # logging.info(f">>> handling the {app_name} webapp")
        # logging.info(f">>> max files for the {app_name} webapp: {maxAllowedUploadedFiles}")
        # logging.info(f">>> received the following identifiers: {identifiers}")
        # logging.info(f"app_handlers[app_name]: {app_handlers[app_name]}")
        
        if amountUploadedFiles > maxAllowedUploadedFiles:
            logging.error(f"uploadFileError.tooManyFiles: client uploaded {amountUploadedFiles}. Max allowed is: {maxAllowedUploadedFiles}")
            return respond_client('tooManyFiles', 413)

        # logging.info(f">>> uploaded {amountUploadedFiles} files")
        # logging.info(f">>> uploaded files: {[file.filename for file in files]}")

        allowed_extensions = get_allowed_extensions(app_name)
        # logging.info(f">>> allowed extensions for this webapp: {allowed_extensions}")

        for file in files:
            if file.filename.split(".").pop() not in allowed_extensions:
                logging.error(f"uploadFileError.badExtension: client uploaded {file.filename}. Extension not allowed.")
                return respond_client('badExtension', 400)


        files_bundle = {ident: file for file, ident in zip(files, identifiers)}
        # logging.info(f">>> files bundle: {files_bundle}")
        
        zip_file_path = app_handlers[app_name](files_bundle)
        
        if zip_file_path:
            try:
                directory = os.path.dirname(zip_file_path)
                filename = os.path.basename(zip_file_path)

                return send_from_directory(directory=directory, path=filename, as_attachment=True)
            except Exception as e:
                logging.error(f"Error in sending file: {e}")
                return respond_client('Failed to send zip file', 500)
        else:
            return respond_client('Failed to process files', 500)
        
        #return respond_client(f'Processed the following files: {files}', 200)

    except RequestEntityTooLarge as e:
        return respond_client('tooLargeRequest', 413)
    except Exception as e:
        logging.error(f"uploadFileError.genericError: {e}")
        return respond_client('internalServerError', 500)


# Run the web app
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
