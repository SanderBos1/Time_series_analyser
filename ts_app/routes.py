from ts_app import app
from flask import request, render_template, session, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from ts_python.files import get_files, remove_files
from ts_python.data_handeling import show_columns, show_image, calculate_pvalue_trend, calculate_pvalue_seasonality
from ts_python.forms import ts_image_form, seasonality_form, trend_form

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
    form = ts_image_form()
    files = get_files(app.config['UPLOAD_FOLDER'])
    if "draw_tsImage" in request.form:
        template = "display_ts.html"
        show_image(files, template, form)
    if "ts_file" in request.form:
        csv = request.form.get("ts_file")
        show_columns(csv)
    if "delete_file" in request.form:
        files = remove_files(request, files)
        return render_template("display_ts.html", files=files, form=form)
    return render_template("display_ts.html", files=files, form=form)

@app.route("/calculations", methods=["GET", "POST"])
def calculations():
    form = seasonality_form()
    form2 = trend_form()
    files = get_files(app.config['UPLOAD_FOLDER'])
    if "ts_file" in request.form:
        csv = request.form.get("ts_file")
        show_columns(csv)
    if "delete_file" in request.form:
        files = remove_files(request, files)
        return render_template("sequencing.html", files=files, form=form, form2=form2)
    if "calculate_trend" in request.form:
        calculate_pvalue_trend(form, form2, files)
    if "calculate_seasonality" in request.form:
        calculate_pvalue_seasonality(files, form, form2)
    if "non_stationary" in request.form:
        session["non_stationary"] = request.form.get("non_stationary")
    return render_template("sequencing.html", files=files, form=form, form2=form2)
