import os
import pandas as pd
from enum import Enum

class PlqSimOperation(Enum):
    ENERGY_LEVEL = "energy_level"
    DONOR_EXCITATION = "donor_excitation"
    ACCEPTOR_EXCITATION = "acceptor_excitation"

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

    except Exception :
        raise

def execute_plqsim_operation(plqSimOperation, xif, appdir):
    return create_result_folder(xif, appdir)