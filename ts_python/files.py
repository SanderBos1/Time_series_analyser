from ts_app import app
import os
import glob
from flask import session

#reads all files from given directory and puts the names in a list
def get_files(target):
    csvFiles = [os.path.basename(x) for x in glob.glob(target + '/*.csv')]
    return csvFiles

def remove_files(request, files):
    csv = request.form.get("delete_file")
    remove_file = app.config['UPLOAD_FOLDER'] + csv
    os.remove(remove_file)
    files.remove(request.form.get("delete_file"))
    if session['dataset'] == csv:
        session.pop('dataset')
        session.pop('ts_columns')
    return files