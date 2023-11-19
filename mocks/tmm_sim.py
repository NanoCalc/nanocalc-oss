import os
import pandas as pd

def calculation(xif, appdir, inputDir):
    try:
        RESULT_FOLDER = os.path.join(appdir, "tmmsim", "result")
        input_tmm = pd.read_excel(xif)
        
        device = input_tmm.iloc[15, 2]
        active_layer_bhj = input_tmm.iloc[22, 1]
        
        new_folder = os.path.join(RESULT_FOLDER,f'TMM_')
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        return f"{os.path.abspath(new_folder)}" 

    except Exception as e:
        print("Error in tmm_sim.py:", e)
