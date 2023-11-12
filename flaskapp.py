from fret_calc import overlap_calculation
from ri_calc import n_calculation, n_k_calculation
from plq_sim import energy_level, donor_excitation, acceptor_excitation
from tmm_sim import calculation
import os 
import zipfile
import uuid
from flask_caching import Cache
from waitress import serve
from flask import Flask, request, url_for, send_from_directory ,render_template, jsonify
from werkzeug.utils import secure_filename
from functools import wraps

# Creates the web app 
app = Flask(__name__)

# App configuration
UPLOAD_FOLDER = '/app/upload'
MAX_CONTENT_LENGTH = 1 * 1024 * 1024    # 1 MB file size limit
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

# Cache configuration
app.config['CACHE_TYPE'] = 'simple'  
cache = Cache(app)


def allowed_file(filename, ext):
    """Returns True if the file extension is in the list of allowed extensions"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ext

def save_file_with_uuid(directory, file, extension):
    """Save a file with a UUID-based name and return its path."""
    filename = f"{uuid.uuid4()}.{extension}"
    filepath = os.path.join(directory, filename)
    file.save(filepath)
    return filepath

def generate_zip(path, webapp):
    """Generate a zip file from a directory and return its name"""
    zip_file_name = f"{uuid.uuid4()}-generated-data.zip"
    zip_file_path = os.path.join(UPLOAD_FOLDER, webapp, zip_file_name)
    with zipfile.ZipFile(zip_file_path, mode="w") as z:
        for filename in os.listdir(path): 
            file_path = os.path.join(path, filename)
            z.write(file_path, arcname=filename)
    return zip_file_name

def log_vistor(f):
    """Decorator to log the amount of unique visitors to the website"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        ip = request.remote_addr
        ips_path = os.path.join(app.root_path,'visitors.txt')
        with open(ips_path, 'a+') as file:
            if ip not in file.read():
                file.write(ip + '\n')
        return f(*args, **kwargs)
    return wrapper


# Main/Home view
@app.route('/', methods = ['GET'])
@log_vistor
def welcome():
    return render_template("index.html")

# About us view 
@app.route('/about', methods = ['GET'])
@cache.cached(timeout=86400)
def about_us():
    return render_template("about.html")

# Entry point to get the unique visitor count   
@app.route('/api/ipcount', methods = ['GET'])
def get_ip_count():
    ips_path = os.path.join(app.root_path,'visitors.txt') 
    with open(ips_path, 'r') as file:
        ip_addresses = file.read().splitlines()

    unique_ip_count = len(ip_addresses)
    return jsonify({'count': unique_ip_count})

# FRET Calculator - initial view
@app.route('/fret', methods=['GET'])
def fret_calc():           
    return render_template("fret.html")

# FRET Calculator - data upload
@app.route('/fret/submit', methods=['POST'])
def fret_calc_submit():
    appName = "FRET-Calc"
    webapp = "fret"

    form_list = []

    files = request.files.getlist("xif") 
    for file in files:
        if allowed_file(file.filename,['xlsx']):
            xif = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'fret', 'index_files'), file, 'xlsx')
            form_list.append(xif)
        else:
            return render_template("input_error.html", data={
                "error": "file_type",
                "file_name": "index file",
                "expected_ext": "xlsx",
                "redirect": "fret"
            })
                                
    files = request.files.getlist("ef")
    for file in files:
        if allowed_file(file.filename,['dat']):
            ef = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'fret', 'emission_files'), file, 'dat')
            form_list.append(ef)
        else:
            return render_template("input_error.html", data={
                "error": "file_type",
                "file_name": "emission file",
                "expected_ext": "dat",
                "redirect": "fret"
            })
        
    files = request.files.getlist("rfi")
    for file in files: 
        if allowed_file(file.filename,['dat']):
            rfi = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'fret', 'refractive_index_files'), file, 'dat')
            form_list.append(rfi)
        else:
            return render_template("input_error.html", data={
                "error": "file_type",
                "file_name": "refractive index file",
                "expected_ext": "dat",
                "redirect": "fret"
            })
    
    files = request.files.getlist("ecf")
    for file in files: 
        if allowed_file(file.filename,['dat']):
            ecf = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'fret', 'extinction_coefficient_files'), file, 'dat')
            form_list.append(ecf)
        else:
            return render_template("input_error.html", data={
                "error": "file_type",
                "file_name": "extinction coefficient file",
                "expected_ext": "dat",
                "redirect": "fret"
            })
    
    data = overlap_calculation(form_list[0], form_list[3], form_list[1], form_list[2], UPLOAD_FOLDER)
    zip_file_name = generate_zip(data, webapp)
    return render_template("upload_success.html", zip_name=zip_file_name, app_name=appName, webapp=webapp)


# Route to allow download of generated data
@app.route('/download/<webapp>/<path:name>', methods=['GET'])
def get_data(webapp, name):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], webapp) 
    return send_from_directory(directory=uploads, path=name)

# RI Calculator view
@app.route('/ricalc', methods=['GET', 'POST'])
def ri_calc():
    appName = "RI-Calc"
    webapp = "ri"
    if request.method == "POST":
        form_list = []
        
        if not request.files.getlist("kf"):
            files = request.files.getlist("xif")
            for file in files:
                if allowed_file(file.filename,['xlsx']):
                    xif = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'ri', 'index_files'), file, 'xlsx')
                    form_list.append(xif)
                else:
                    return render_template("input_error.html", data={
                        "error": "file_type",
                        "file_name": "index file",
                        "expected_ext": "xlsx",
                        "redirect": "ricalc"
                    })
                    
            files = request.files.getlist("dacf")
            for file in files:
                if allowed_file(file.filename,['dat']):
                    dacf = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'ri', 'abs_coefficient_files'), file, 'dat')
                    form_list.append(dacf)
                else:
                    return render_template("input_error.html", data={
                        "error": "file_type",
                        "file_name": "abs coefficient file",
                        "expected_ext": "dat",
                        "redirect": "ricalc"
                    })

               
            data_n_k = n_k_calculation(form_list[0], form_list[1], UPLOAD_FOLDER)
            zip_file_name = generate_zip(data_n_k, webapp)
            return render_template("upload_success.html", zip_name=zip_file_name,  app_name=appName, webapp=webapp)    


        elif not request.files.getlist("dacf"):
            files = request.files.getlist("xif")
            for file in files:
                if allowed_file(file.filename,['xlsx']):
                    xif = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'ri', 'index_files'), file, 'xlsx')
                    form_list.append(xif)
                else:
                    return render_template("input_error.html", data={
                        "error": "file_type",
                        "file_name": "index file",
                        "expected_ext": "xlsx",
                        "redirect": "ricalc"
                    })
                    

            files = request.files.getlist("kf")
            for file in files:
                if allowed_file(file.filename,['dat']):
                    kf = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'ri', 'k_files'), file, 'dat')
                    form_list.append(kf)
                else:
                    return render_template("input_error.html", data={
                        "error": "file_type",
                        "file_name": "K file",
                        "expected_ext": "dat",
                        "redirect": "ricalc"
                    })
                    
            data_n = n_calculation(form_list[0], form_list[1], UPLOAD_FOLDER)
            zip_file_name = generate_zip(data_n, webapp) 
            return render_template("upload_success.html", zip_name=zip_file_name,  app_name=appName, webapp=webapp) 
            
    return render_template("ricalc.html")

# PLQSim view
@app.route('/plqsim', methods=['GET', 'POST'])
def plq_sim():
    appName = "PLQSim"
    webapp = "plqsim"
    if request.method == "POST":
        index_file = request.files.getlist("xif")
        for file in index_file:
            if allowed_file(file.filename,['xlsx']):
                xif = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'plqsim', 'input_files'), file, 'xlsx')
            else:
                return render_template("input_error.html", data={
                    "error": "file_type",
                    "file_name": "index file",
                    "expected_ext": "xlsx",
                    "redirect": "plqsim"
                })

        energy_level(xif, UPLOAD_FOLDER) # Generate Energy Level plot for both choices
        action = request.form.get('action')

        if action == 'Calculate Acceptor Excitation':
            data = acceptor_excitation(xif, UPLOAD_FOLDER)
            zip_file_name = generate_zip(data, webapp)
        elif action == 'Calculate Donor Excitation':
            data = donor_excitation(xif,UPLOAD_FOLDER)
            zip_file_name = generate_zip(data,webapp)

        return render_template("upload_success.html", zip_name=zip_file_name,  app_name=appName, webapp=webapp)

    return render_template("plqsim.html")

# TMMSim view 
@app.route('/tmmsim', methods=['GET', 'POST'])
def tmm_sim():
    appName = "TMMSim"
    webapp = "tmmsim"
    if request.method == "POST":
        xif = request.files["xif"]
        if xif and allowed_file(xif.filename, ['xlsx']):
            xif = save_file_with_uuid(os.path.join(app.config['UPLOAD_FOLDER'], 'tmmsim' ,'input_files'), xif, 'xlsx')
        else:
            return render_template("input_error.html", data={
                "error": "file_type",
                "file_name": "index file",
                "expected_ext": "xlsx",
                "redirect": "tmmsim"
            })

        layer_files = request.files.getlist("layer_files")
        if len(layer_files) > 10:
            return render_template("input_error.html", data={
                "error": "file_count",
                "redirect": "tmmsim"
            })

        csv_paths = []
        for file in layer_files:
            if allowed_file(file.filename, ['csv']):
                csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'tmmsim' ,'input_files', secure_filename(file.filename))
                file.save(csv_path)
                csv_paths.append(csv_path)
            else:
                return render_template("input_error.html", data={
                    "error": "file_type",
                    "file_name": "layer file",
                    "expected_ext": "csv",
                    "redirect": "tmmsim"
                })
        

        input_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'tmmsim' ,'input_files')
        data = calculation(xif, UPLOAD_FOLDER, input_dir)
        zip_file_name = generate_zip(data, webapp)

        return render_template("upload_success.html", zip_name=zip_file_name, app_name=appName, webapp=webapp)

    return render_template("tmmsim.html")

# Energy Unit Converter view 
@app.route('/euconverter', methods=['GET'])
@cache.cached(timeout=86400)
def eu_converter():
    return render_template("euconverter.html")


# Run the web app
if __name__ == "__main__":
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'

    if debug_mode:
        app.run(
            host='0.0.0.0',
            port=80,
            debug=True,
        )
    else:
        serve(app)
