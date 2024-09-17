import os
import pandas as pd

def create_folder(xif, folder_suffix, appdir):
    try:
        RESULT_FOLDER = os.path.join(appdir, "ricalc", "result")
        input_kk = pd.read_excel(xif)

        name = input_kk.iloc[0, 1]
        unity = input_kk.iloc[2, 1]

        new_folder = os.path.join(RESULT_FOLDER, f'nk_{name}_{folder_suffix}')
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        return os.path.abspath(new_folder)
        
    except Exception:
        raise

def n_calculation(xif, kf, appdir):
    return create_folder(xif, 'from_k', appdir)

def n_k_calculation(xif, dacf, appdir):
    return create_folder(xif, 'from_Abs_Coef', appdir)
