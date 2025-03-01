from computation_handlers import handle_fretcalc, handle_ricalc, handle_plqsim, handle_tmmsim
import logging

def run_heavy_task(app_name, files_bundle, job_id, directory_for_app):
    """
    This function runs in the background (in the RQ worker).
    It calls the correct handler function based on 'app_name',
    does the same logic, and returns the path to the resulting ZIP.
    """

    zip_file_path = None
    if app_name == 'fretcalc':
        zip_file_path = handle_fretcalc(files_bundle, directory_for_app)
    elif app_name == 'ricalc':
        zip_file_path = handle_ricalc(files_bundle, directory_for_app)
    elif app_name == 'plqsim':
        zip_file_path = handle_plqsim(files_bundle, directory_for_app)
    elif app_name == 'tmmsim':
        zip_file_path = handle_tmmsim(files_bundle, directory_for_app)
    else:
        logging.error(f"Unknown app_name: {app_name}")

    return zip_file_path
