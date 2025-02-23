from apps_definitions import get_max_files, get_allowed_extensions
from computation_handlers import handle_fretcalc, handle_ricalc, handle_plqsim, handle_tmmsim
import logging
import os

def run_heavy_task(app_name, files_bundle, job_id):
    """
    This function runs in the background (in the RQ worker).
    It calls the correct handler function based on 'app_name',
    does the same logic, and returns the path to the resulting ZIP.
    """
    logging.info(f"Starting heavy task for job_id={job_id} app_name={app_name}")
    # This calls your existing “handle_*” logic
    zip_file_path = None
    if app_name == 'fretcalc':
        zip_file_path = handle_fretcalc(files_bundle)
    elif app_name == 'ricalc':
        zip_file_path = handle_ricalc(files_bundle)
    elif app_name == 'plqsim':
        zip_file_path = handle_plqsim(files_bundle)
    elif app_name == 'tmmsim':
        zip_file_path = handle_tmmsim(files_bundle)
    else:
        logging.error(f"Unknown app_name: {app_name}")

    return zip_file_path
