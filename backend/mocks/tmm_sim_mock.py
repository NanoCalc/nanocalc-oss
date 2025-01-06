import os
import pandas as pd

def calculation(input_tmm_filepath, input_tmm_filename, output_folder_path, status_callback):
    try:
        RESULT_FOLDER = os.path.join(output_folder_path, "tmmsim", "result")
        input_tmm = pd.read_excel(input_tmm_filename)
        
        device = input_tmm.iloc[15, 2]
        active_layer_bhj = input_tmm.iloc[22, 1]
        
        new_folder = os.path.join(RESULT_FOLDER,f'TMM_')
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        return f"{os.path.abspath(new_folder)}" 

    except Exception:
        raise
