from bppimt_farewell_backend.settings import BASE_DIR
import os

# THE FILE TYPE OF CONFESSION AUDIO FILES...RIGHT NOW THIS IS THE ONLY TYPE OF FILE EXTENSION THAT WILL BE ACCEPTED
CONFESSION_FILE_EXTENSION='.mp3'

#Location for copying of the temporary files which were uploaded

def get_local_uploaded_files_path():
    FILE_UPLOAD_DIR=BASE_DIR+'/uploaded_files/'
    if not os.path.isdir(FILE_UPLOAD_DIR):
        os.makedirs(FILE_UPLOAD_DIR)
    return FILE_UPLOAD_DIR