import os
import pandas as pd

def n_calculation(xif, kf, appdir):
    try:
        RESULT_FOLDER = os.path.join(appdir, "ri", "result")
        input_kk = pd.read_excel(xif)

        name = input_kk.iloc[0, 1]
        unity = input_kk.iloc[2, 1]

        new_folder = os.path.join(RESULT_FOLDER,f'nk_{name}_from_Abs_Coef')
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        return f"{os.path.abspath(new_folder)}" 

    except Exception as e:
        print("Error in ri_calc.py:", e)
    
def n_k_calculation(xif, dacf, appdir):
    try:
        RESULT_FOLDER = os.path.join(appdir, "ri", "result")
        input_kk = pd.read_excel(xif)
        
        name = input_kk.iloc[0, 1]
        unity = input_kk.iloc[2, 1]

        new_folder = os.path.join(RESULT_FOLDER,f'nk_{name}_from_Abs_Coef')
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        return f"{os.path.abspath(new_folder)}" 
        
    except Exception as e:
        print("Error in ri_calc.py:", e)
