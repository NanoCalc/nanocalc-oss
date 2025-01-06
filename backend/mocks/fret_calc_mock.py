import os
import pandas as pd

def overlap_calculation(xif, ecf, ef, rfi, appdir, callback = None):
    try:
        RESULT_FOLDER = os.path.join(appdir, "fretcalc", "result")
        input_fret_df = pd.read_excel(xif)
        
        donor_name = input_fret_df.iloc[1, 1]
        acceptor_name = input_fret_df.iloc[5, 1]
        neff = input_fret_df.iloc[10, 1]
        
        new_folder = os.path.join(RESULT_FOLDER,f'FRET-{donor_name}-{acceptor_name}')
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        return f"{os.path.abspath(new_folder)}"  

    except Exception:
        raise
