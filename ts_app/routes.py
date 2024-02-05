from ts_app import app
from flask import request, render_template, session, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from ts_python.files import get_files, remove_files
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
    if "draw_tsImage" in request.form:
        show_image(request, files, "display_ts")
    if "ts_file" in request.form:
        csv = request.form.get("ts_file")
        show_columns(csv)
    if "delete_file" in request.form:
        files = remove_files(request, files)
        return render_template("display_ts.html", files=files)
    return render_template("display_ts.html", files=files)

@app.route("/calculations", methods=["GET", "POST"])
def calculations():
    files = get_files(app.config['UPLOAD_FOLDER'])
    if "ts_file" in request.form:
        csv = request.form.get("ts_file")
        show_columns(csv)
    if "delete_file" in request.form:
        files = remove_files(request, files)
        return render_template("calculations.html", files=files)
    return render_template("calculations.html", files=files)
