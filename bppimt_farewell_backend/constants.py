from bppimt_farewell_backend.settings import BASE_DIR
import os
from ask.models import Ask
from confessions.models import Confessions

# THE FILE TYPE OF CONFESSION AUDIO FILES...RIGHT NOW THIS IS THE ONLY TYPE OF FILE EXTENSION THAT WILL BE ACCEPTED
CONFESSION_FILE_EXTENSION='.mp3'

ACCEPTED_PROFILE_PICTURE_TYPES={'.jpg','.jpeg','.png'}

ALLOWED_MODELS_FOR_LIKE_AND_COMMENT={Ask,Confessions} #This has been done as a safeguard to ensure we dont get any errors while implementing callback functions for post_save() and other signals for Comment model and Like model

#Location for copying of the temporary files which were uploaded

def get_local_uploaded_files_path():
    FILE_UPLOAD_DIR=BASE_DIR+'/uploaded_files/'
    if not os.path.isdir(FILE_UPLOAD_DIR):
        os.makedirs(FILE_UPLOAD_DIR)
    return FILE_UPLOAD_DIR

aws_bucket='bpp-user-files'
aws_folder='v1'