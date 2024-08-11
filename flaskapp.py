from fret_calc import overlap_calculation
from ri_calc import n_calculation, n_k_calculation
from plq_sim import energy_level, donor_excitation, acceptor_excitation
from tmm_sim import calculation
from upload_error import UploadError
from config import Config
from helper_functions import allowed_file, save_file_with_uuid, generate_zip
import os 
import logging
from flask_caching import Cache
from waitress import serve
from flask import Flask, request, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename


# Creating and configuring the Flask app
app = Flask(__name__)
app.config.from_object(Config)
logging.basicConfig(level=Config.LOGGING_LEVEL, format=Config.LOGGING_FORMAT)
cache = Cache(app)
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']


formField = 'NANOCALC_USER_UPLOADED_FILES'

def respond_client(message, code):
    return jsonify({
        'message': message
    }), code

# Client side caching
@app.after_request
def set_cache_headers(response):
    response.headers['Cache-Control'] = 'public, max-age=86400' 
    return response


# Route to allow download of generated data
@app.route('/download/<webapp>/<path:name>', methods=['GET'])
def get_data(webapp, name):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], webapp) 
    return send_from_directory(directory=uploads, path=name)


# FRET Calculator - data upload
@app.route('/fret/submit', methods=['POST'])
def fret_calc_submit():
    appName = "FRET-Calc"
    webApp = "fret"
    filesList = []

    try:
        files = request.files.getlist("xif") 
        for file in files:
            if allowed_file(file.filename,['xlsx']):
                xif = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'fret', 'index_files'), file, 'xlsx')
                filesList.append(xif)
            else:
                upload_error = UploadError("file_type", "index file", "xlsx", "fret")
                return render_template("input_error.html", data=upload_error.to_dict())

        files = request.files.getlist("ef")
        for file in files:
            if allowed_file(file.filename,['dat']):
                ef = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'fret', 'emission_files'), file, 'dat')
                filesList.append(ef)
            else:
                upload_error = UploadError("file_type", "emission file", "dat", "fret")
                return render_template("input_error.html", data=upload_error.to_dict())

        files = request.files.getlist("rfi")
        for file in files: 
            if allowed_file(file.filename,['dat']):
                rfi = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'fret', 'refractive_index_files'), file, 'dat')
                filesList.append(rfi)
            else:
                upload_error = UploadError("file_type", "refractive index file", "dat", "fret")
                return render_template("input_error.html", data=upload_error.to_dict())

        files = request.files.getlist("ecf")
        for file in files: 
            if allowed_file(file.filename,['dat']):
                ecf = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'fret', 'extinction_coefficient_files'), file, 'dat')
                filesList.append(ecf)
            else:
                upload_error = UploadError("file_type", "extinction coefficient file", "dat", "fret")
                return render_template("input_error.html", data=upload_error.to_dict())
        data = overlap_calculation(filesList[0], filesList[3], filesList[1], filesList[2], UPLOAD_FOLDER)
        zip_file_name = generate_zip(data, webApp, Config.UPLOAD_FOLDER)
        return render_template("upload_success.html", zip_name=zip_file_name, app_name=appName, webapp=webApp)

    except Exception as e: 
        logging.warning(f"Error in FRET-Calc: {e}")
        upload_error = UploadError("file_misformat", None, None, "ricalc")
        return render_template("input_error.html", data=upload_error.to_dict())


# RI Calculator - data upload
@app.route('/ricalc/submit', methods=['POST'])
def ri_calc_submit():
    appName = "RI-Calc"
    webApp = "ri"
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

@app.route('/upload', methods=['POST'])
def upload_file():
    requestFiles = request.files

    if formField not in requestFiles:
        return respond_client('emptyRequest', 400)
    
    files = [file for file in requestFiles.getlist(formField) if file.filename]
    logging.info(f">>> uploaded files: {[file.filename for file in files]}")
    return respond_client('Success!', 200)


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
