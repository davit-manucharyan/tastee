import os
import shutil

def save_uploaded_file(file_object, file_path):
    with open(file_path, "wb") as file_dest:
        shutil.copyfileobj(file_object.file, file_dest)
