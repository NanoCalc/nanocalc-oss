import os
import logging

from config import Config
from helper_functions import generate_zip
from fretcalc_core import overlap_calculation
from ricalc_core import n_calculation, n_k_calculation
from plqsim_facade import execute_plqsim_operation, PlqSimOperation
from tmmsim_core import calculation
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = Config.UPLOAD_FOLDER


def handle_fretcalc(files_bundle):
    """
    files_bundle['inputExcel'] is already a string path,
    likewise 'extinctionCoefficient', 'emissionCoefficient', 'refractiveIndex' are paths.
    We simply pass those paths to the calculation and generate the final ZIP.
    """
    fretcalc_folder = os.path.join(UPLOAD_FOLDER, 'fretcalc')

    try:
        input_excel_path = files_bundle['inputExcel']
        extinction_path = files_bundle['extinctionCoefficient']
        emission_path = files_bundle['emissionCoefficient']
        refractive_path = files_bundle['refractiveIndex']


        # Do the overlap calculation
        dataFolderPath = overlap_calculation(
            input_excel_path,
            extinction_path,
            emission_path,
            refractive_path,
            UPLOAD_FOLDER
        )
        # Generate zip
        zip_file_name = generate_zip(dataFolderPath, 'fretcalc', UPLOAD_FOLDER)
        return zip_file_name
    except Exception as e:
        logging.error(f"handle_fretcalc.error: {e}")
        raise e


def handle_ricalc(files_bundle):
    """
    files_bundle['inputExcel'] => path to the input file
    files_bundle['mode'] => 'opticalConstants' or 'refractiveIndex'
    Then we read the relevant coefficient path (already saved).
    """
    ricalc_folder = os.path.join(UPLOAD_FOLDER, 'ricalc')

    try:
        input_excel_path = files_bundle['inputExcel']
        mode = files_bundle.get('mode')  # 'opticalConstants' or 'refractiveIndex'
        dataFolderPath = None

        if mode == 'opticalConstants':
            coefficient_path = files_bundle['decadicCoefficient']
            dataFolderPath = n_k_calculation(input_excel_path, coefficient_path, None, UPLOAD_FOLDER)
        elif mode == 'refractiveIndex':
            coefficient_path = files_bundle['constantK']
            dataFolderPath = n_calculation(input_excel_path, coefficient_path, None, UPLOAD_FOLDER)
        else:
            # TODO: handle error or unexpected mode
            pass

        zip_file_name = generate_zip(dataFolderPath, 'ricalc', UPLOAD_FOLDER)
        return zip_file_name
    except Exception as e:
        logging.error(f"handle_ricalc.error: {e}")
        raise e


def handle_plqsim(files_bundle):
    """
    files_bundle['inputExcel'] => path to the input Excel
    files_bundle['mode'] => 'donorExcitation' or 'acceptorExcitation'
    We call plqsim ops, then create a ZIP.
    """
    plqsim_folder = os.path.join(UPLOAD_FOLDER, 'plqsim')

    try:
        input_excel_path = files_bundle['inputExcel']
        mode = files_bundle.get('mode')
        
        # Always do ENERGY_LEVEL first
        execute_plqsim_operation(PlqSimOperation.ENERGY_LEVEL, input_excel_path, None, UPLOAD_FOLDER)

        if mode == 'donorExcitation':
            dataFolderPath = execute_plqsim_operation(PlqSimOperation.DONOR_EXCITATION, input_excel_path, None, UPLOAD_FOLDER)
        elif mode == 'acceptorExcitation':
            dataFolderPath = execute_plqsim_operation(PlqSimOperation.ACCEPTOR_EXCITATION, input_excel_path, None, UPLOAD_FOLDER)
        else:
            # TODO: handle unknown mode
            dataFolderPath = None
        
        zip_file_name = generate_zip(dataFolderPath, 'plqsim', UPLOAD_FOLDER)
        return zip_file_name
    except Exception as e:
        logging.error(f"handle_plqsim.error: {e}")
        raise e


def handle_tmmsim(files_bundle):
    """
    files_bundle['inputExcel'] => path
    files_bundle['layerFiles'] => list of CSV file paths
    We pass them along to the TMM calculation if needed.
    """
    tmmsim_folder = os.path.join(UPLOAD_FOLDER, 'tmmsim')

    try:
        input_excel_path = files_bundle['inputExcel']
        layer_files = files_bundle.get('layerFiles', [])

        # We already saved those CSVs in the route, so there's no need to re-save them here.
        # If the 'calculation' function needs the actual path, we already have them in layer_files.

        # For example, if you need them for 'calculation', you could pass them in or do something like:
        # dataFolderPath = calculation(tmmsim_folder, input_excel_path, UPLOAD_FOLDER, layer_files)
        # But if your existing 'calculation' function only needs input_excel_path + UPLOAD_FOLDER, keep it as is.
        
        dataFolderPath = calculation(tmmsim_folder, input_excel_path, UPLOAD_FOLDER, None)
        zip_file_name = generate_zip(dataFolderPath, 'tmmsim', UPLOAD_FOLDER)
        return zip_file_name
    except Exception as e:
        logging.error(f"handle_tmmsim.error: {e}")
        raise e
