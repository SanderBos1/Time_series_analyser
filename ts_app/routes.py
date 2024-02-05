from ts_app import app
from flask import request, render_template, session, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from ts_python.files import get_files
from ts_python.data_handeling import show_columns, show_image


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=["GET", "POST"])
def hello():
    if  'datasetCSV' in request.form:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("home.html")


@app.route('/display_ts', methods=["GET", "POST"])
def display_ts():
    files = get_files(app.config['UPLOAD_FOLDER'])
    file_list = []
    for file in files:
        file_list.append(file.split(".csv")[0])
    if "draw" in request.form:
        show_image(request, file_list, "display_ts")
    if "ts_file" in request.form:
        csv = request.form.get("ts_file")
        show_columns(csv)
    return render_template("display_ts.html", file_list=file_list)

@app.route("/calculations", methods=["GET", "POST"])
def calculations():
    files = get_files(app.config['UPLOAD_FOLDER'])
    file_list = []
    for file in files:
        file_list.append(file.split(".csv")[0])
    if "ts_file" in request.form:
        csv = request.form.get("ts_file")
        show_columns(csv)
    return render_template("calculations.html", file_list=file_list)
