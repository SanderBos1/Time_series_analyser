from flask import current_app
import os
import glob
from flask import session

#reads all files from given directory and puts the names in a list
def get_files(target):
    csvFiles = [os.path.basename(x) for x in glob.glob(target + '/*.csv')]
    return csvFiles

def remove_files(request, files):
    csv = request.form.get("delete_file")
    remove_file = current_app.config['UPLOAD_FOLDER'] + csv
    os.remove(remove_file)
    files.remove(request.form.get("delete_file"))
    if session.get("dataset") is None:
        return files
    if session['dataset'].get_file_name() == csv:
        for key in list(session.keys()):
            session.pop(key)
    return files