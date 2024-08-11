allowed_extensions = {
    'fretcalc': {'xlsx': 1, 'dat': 3},
    'ricalc': {'xlsx': 1, 'dat': 1},
    'plqsim': {'xlsx': 1},
    'tmmsim': {'xlsx': 1, 'csv': 10}
}

def get_max_files(app_name):
    extensions = allowed_extensions.get(app_name)
    if extensions is not None:
        count = sum(extensions.values())
        return count
    return 0 
