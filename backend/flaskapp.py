import os 
import logging_config
import logging
from waitress import serve
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from apps_definitions import get_max_files, get_allowed_extensions
from config import Config
import redis
from rq import Queue
import uuid
from tasks import run_heavy_task
from rq.job import Job


app = Flask(__name__)
app.config.from_object(Config)

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
FILE_ID_FORM_FIELD = 'NANOCALC_FILE_ID_FORM_FIELD'
FILES_FORM_FIELD = 'NANOCALC_USER_UPLOADED_FILES'
MODE_FORM_FIELD = 'NANOCALC_USER_MODE'

redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
conn = redis.from_url(redis_url)
q = Queue("default", connection=conn)


def respond_client(message, code):
    return jsonify({
        'message': message
    }), code


@app.route('/health', methods=['GET'])
def health():
    return respond_client('Up and running!', 200)

@app.route("/status/<job_id>", methods=["GET"])
def check_status(job_id):
    try:
        job = Job.fetch(job_id, connection=conn)
    except Exception as e:
        # RQ throws an error if job not found in Redis
        logging.error(f"/status/<job_id> route check_status RQ exception: {e}")
        return jsonify({"status": "not_found"}), 404

    if job.is_queued:
        return jsonify({"status": "queued"}), 200
    elif job.is_started:
        return jsonify({"status": "in-progress"}), 200
    elif job.is_finished:
        return jsonify({"status": "finished"}), 200
    elif job.is_failed:
        return jsonify({"status": "failed"}), 200
    else:
        return jsonify({"status": "unknown"}), 200

@app.route("/download/<job_id>", methods=["GET"])
def download_result(job_id):

    try:
        job = Job.fetch(job_id, connection=conn)
    except Exception as e:
        logging.error(f"/download/<job_id> route download_result RQ exception: {e}")
        return jsonify({"error": "job not found"}), 404
    
    if not job.is_finished:
        return jsonify({"error": f"Job not finished; status={job.get_status()}"}), 400

    # The path to the ZIP was returned by run_heavy_task
    zip_file_path = job.result  
    # job.result is whatever run_heavy_task(...) returned
    
    if not zip_file_path or not os.path.exists(zip_file_path):
        return jsonify({"error": "no result file found"}), 404

    # Serve the file
    # can also use send_from_directory if you want
    return send_file(zip_file_path, as_attachment=True)


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
        directory_for_app = os.path.join(UPLOAD_FOLDER, app_name, f"{uuid.uuid4()}")
        os.makedirs(directory_for_app, exist_ok=True)
        for file_id, file in zip(file_ids, files):
            secure_name = secure_filename(file.filename)
            saved_path = os.path.join(directory_for_app, secure_name)

            file.save(saved_path)

            if file_id == 'layerFiles':
                if file_id not in files_bundle:
                    files_bundle[file_id] = []
                files_bundle[file_id].append(saved_path)
            else:
                files_bundle[file_id] = saved_path

        mode = requestForm.get(MODE_FORM_FIELD)
        if mode:
            files_bundle['mode'] = mode
        
        job_id = str(uuid.uuid4())
        job = q.enqueue(
            run_heavy_task,
            app_name,
            files_bundle,
            job_id,
            directory_for_app,
            job_timeout=1200
        )

        return jsonify({
            "status": "queued",
            "job_id": job.get_id()
        }), 202

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
