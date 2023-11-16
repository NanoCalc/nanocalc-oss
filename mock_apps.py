def overlap_calculation(xif, ecf, ef, rfi, appdir):
    RESULT_FOLDER = os.path.join(appdir,"fret","result")
    new_folder = os.path.join(RESULT_FOLDER,f'FRET-{donor_name}-{acceptor_name}')
    return f"{os.path.abspath(new_folder)}"  

def n_calculation():
    RESULT_FOLDER = os.path.join(appdir,"ri","result")
    new_folder = os.path.join(RESULT_FOLDER,f'nk_{name}_from_Abs_Coef')
    return f"{os.path.abspath(new_folder)}" 
    
def n_k_calculation():
    RESULT_FOLDER = os.path.join(appdir,"ri","result")
    new_folder = os.path.join(RESULT_FOLDER, f'nk_{name}_from_k')
    return f"{os.path.abspath(new_folder)}" 

def energy_level():
    RESULT_FOLDER = os.path.join(appdir,"plqsim","result")
    new_folder = os.path.join(RESULT_FOLDER,f'PLQuenching-{donor_name}-{acceptor_name}')
    return f"{os.path.abspath(new_folder)}" 

def donor_excitation(): 
    RESULT_FOLDER = os.path.join(appdir,"plqsim","result")
    new_folder = os.path.join(RESULT_FOLDER,f'PLQuenching-{donor_name}-{acceptor_name}')
    return f"{os.path.abspath(new_folder)}" 

def acceptor_excitation():
    RESULT_FOLDER = os.path.join(appdir,"plqsim","result")
    new_folder = os.path.join(RESULT_FOLDER,f'PLQuenching-{donor_name}-{acceptor_name}')
    return f"{os.path.abspath(new_folder)}" 

def calculation():
    RESULT_FOLDER = os.path.join(appdir,"tmmsim","result")
    new_folder = os.path.join(RESULT_FOLDER,f'TMM_{device_type}_{name_bhj}_{name_bilayer}')
    return f"{os.path.abspath(new_folder)}" 
