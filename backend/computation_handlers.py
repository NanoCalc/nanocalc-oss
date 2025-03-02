import os
import logging_config
import logging
from helper_functions import generate_zip
from fretcalc_core import overlap_calculation
from ricalc_core import n_calculation, n_k_calculation
from plqsim_facade import execute_plqsim_operation, PlqSimOperation
from tmmsim_core import calculation


def handle_fretcalc(files_bundle, input_fretcalc_filepath):
    fretcalc_result_folder = os.path.join(input_fretcalc_filepath, "result")
    os.makedirs(fretcalc_result_folder, exist_ok=True)

    try:
        input_excel_path = files_bundle['inputExcel']
        extinction_path = files_bundle['extinctionCoefficient']
        emission_path = files_bundle['emissionCoefficient']
        refractive_path = files_bundle['refractiveIndex']

        dataFolderPath = overlap_calculation(
            input_excel_path,
            extinction_path,
            emission_path,
            refractive_path,
            fretcalc_result_folder
        )
        
        zip_file_name = generate_zip(dataFolderPath, fretcalc_result_folder)
        return zip_file_name
    except Exception as e:
        logging.error(f"handle_fretcalc.error: {e}")
        raise e


def handle_ricalc(files_bundle, input_ricalc_filepath):
    ricalc_result_folder = os.path.join(input_ricalc_filepath, "result")
    os.makedirs(ricalc_result_folder, exist_ok=True)

    try:
        input_excel_path = files_bundle['inputExcel']
        mode = files_bundle.get('mode')

        if mode == 'opticalConstants':
            coefficient_path = files_bundle['decadicCoefficient']
            dataFolderPath = n_k_calculation(input_excel_path, coefficient_path, None, ricalc_result_folder)
        elif mode == 'refractiveIndex':
            coefficient_path = files_bundle['constantK']
            dataFolderPath = n_calculation(input_excel_path, coefficient_path, None, ricalc_result_folder)
        else:
            raise ValueError(f"unexptected ricalc mode: {mode}")

        zip_file_name = generate_zip(dataFolderPath, ricalc_result_folder)
        return zip_file_name
    except Exception as e:
        logging.error(f"handle_ricalc.error: {e}")
        raise e


def handle_plqsim(files_bundle, input_plqsim_filepath):
    plqsim_result_folder = os.path.join(input_plqsim_filepath, "result")
    os.makedirs(plqsim_result_folder, exist_ok=True)

    try:
        input_excel_path = files_bundle['inputExcel']
        mode = files_bundle.get('mode')
        
        # Calculate the energy level for both choices
        execute_plqsim_operation(PlqSimOperation.ENERGY_LEVEL, input_excel_path, None, plqsim_result_folder)

        if mode == 'donorExcitation':
            dataFolderPath = execute_plqsim_operation(PlqSimOperation.DONOR_EXCITATION, input_excel_path, None, plqsim_result_folder)
        elif mode == 'acceptorExcitation':
            dataFolderPath = execute_plqsim_operation(PlqSimOperation.ACCEPTOR_EXCITATION, input_excel_path, None, plqsim_result_folder)
        else:
            raise ValueError(f"unexptected plqsim mode: {mode}")
        
        zip_file_name = generate_zip(dataFolderPath, plqsim_result_folder)
        return zip_file_name
    except Exception as e:
        logging.error(f"handle_plqsim.error: {e}")
        raise e


def handle_tmmsim(files_bundle, input_tmmsim_filepath):
    tmm_result_folder = os.path.join(input_tmmsim_filepath, "result")
    os.makedirs(tmm_result_folder, exist_ok=True)

    try:
        input_tmm_filename = files_bundle['inputExcel']
        
        dataFolderPath1, dataFolderPath2 = calculation(input_tmmsim_filepath, input_tmm_filename, tmm_result_folder, None)
        zip_file_name = generate_zip([dataFolderPath1, dataFolderPath2], tmm_result_folder)
        return zip_file_name
    except Exception as e:
        logging.error(f"handle_tmmsim.error: {e}")
        raise e
