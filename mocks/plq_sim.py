import os
import pandas as pd

def energy_level(xif, appdir):
    try:

        RESULT_FOLDER = os.path.join(appdir,"plqsim","result")
        input_df = pd.read_excel(xif)

        # Materials names
        donor_name = input_df.iloc[2, 1]
        acceptor_name = input_df.iloc[9, 1]
        new_folder = os.path.join(RESULT_FOLDER,f'PLQuenching-')
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        return f"{os.path.abspath(new_folder)}" 
    except Exception as e:
        print("Error in plq_sim.py:", e)
        

def donor_excitation(xif, appdir): 
    try:
        RESULT_FOLDER = os.path.join(appdir,"plqsim","result")
        # Reading input parameters
        input_df = pd.read_excel(xif)
        # Temperature (K)
        temp = input_df.iloc[0, 1]
        # Materials names
        donor_name = input_df.iloc[2, 1]
        acceptor_name = input_df.iloc[9, 1]
        new_folder = os.path.join(RESULT_FOLDER,f'PLQuenching-')
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        return f"{os.path.abspath(new_folder)}" 
    except Exception as e:
        print("Error in plq_sim.py:", e)

def acceptor_excitation(xif, appdir):
    try:
        RESULT_FOLDER = os.path.join(appdir,"plqsim","result")
        # Reading input parameters
        input_df = pd.read_excel(xif)
        # Temperature (K)
        temp = input_df.iloc[0, 1]
        # Materials names
        donor_name = input_df.iloc[2, 1]
        acceptor_name = input_df.iloc[9, 1]
        new_folder = os.path.join(RESULT_FOLDER,f'PLQuenching-')
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        return f"{os.path.abspath(new_folder)}" 
    except Exception as e:
        print("Error in plq_sim.py:", e)
