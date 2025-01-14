import os
import shutil

def create_new_path(old_path, new_dir, id):

    old_path_base = os.path.basename(old_path)
    file_extension = old_path_base.split('.')[-1]
    new_path = new_dir + "\\" + id + "." + file_extension

    return new_path

def copy_receipt_imagefiles(source_path, destination_path):
    shutil.copy(source_path, destination_path)

