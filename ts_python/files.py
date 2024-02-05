from ts_app import app
import os
import glob

#reads all files from given directory and puts the names in a list
def get_files(target):
    csvFiles = [os.path.basename(x) for x in glob.glob(target + '/*.csv')]
    return csvFiles

def remove_files(request, files):
    remove_file = app.config['UPLOAD_FOLDER'] + request.form.get("delete_file")
    os.remove(remove_file)
    files.remove(request.form.get("delete_file"))
    return files