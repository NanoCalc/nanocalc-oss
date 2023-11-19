import os
import pandas as pd

def create_result_folder(xif, appdir):
    try:
        RESULT_FOLDER = os.path.join(appdir, "plqsim", "result")
        input_df = pd.read_excel(xif)

        donor_name = input_df.iloc[2, 1]
        acceptor_name = input_df.iloc[9, 1]

        new_folder = os.path.join(RESULT_FOLDER, 'PLQuenching-')
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        return os.path.abspath(new_folder)

    except Exception as e:
        print("Error in creating result folder:", e)
        return None

def energy_level(xif, appdir):
    return create_result_folder(xif, appdir)

def donor_excitation(xif, appdir):
    return create_result_folder(xif, appdir)

def acceptor_excitation(xif, appdir):
    return create_result_folder(xif, appdir)
