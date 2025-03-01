import os
import zipfile

def generate_zip(sourceDir, targetDir):
    """
    Generate a zip file with all the visible content from a source directory,
    receive the targetDir where the zip file will be stored.
    """
    zip_file_path = os.path.join(targetDir, "generated-data.zip")

    os.makedirs(targetDir, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, mode="w") as z:
        for filename in os.listdir(sourceDir): 
            file_path = os.path.join(sourceDir, filename)
            z.write(file_path, arcname=filename)

    return zip_file_path
    