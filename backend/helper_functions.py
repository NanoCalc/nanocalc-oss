import os
import zipfile

def generate_zip(sourceDir, targetDir):
    """
    Generate a zip file with all the visible content from a source directory,
    receive the targetDir where the zip file will be stored.
    """
    # Normalize input
    if isinstance(sourceDir, (list, tuple)):
        source_dirs = sourceDir
    else:
        source_dirs = [sourceDir]

    zip_file_path = os.path.join(targetDir, "generated-data.zip")
    os.makedirs(targetDir, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, mode="w") as z:
        for dir_path in source_dirs:
            for filename in os.listdir(dir_path):
                file_path = os.path.join(dir_path, filename)
                z.write(file_path, arcname=filename)

    return zip_file_path
    