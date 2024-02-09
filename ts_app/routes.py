from ts_app import app
from flask import request, render_template, session, flash
from werkzeug.utils import secure_filename
import os
from ts_python.files import get_files, remove_files
from ts_python.data_handeling import show_image, calculate_pvalue_trend, calculate_pvalue_seasonality
from ts_python.forms import ts_image_form, seasonality_form, trend_form, granger_causality_form
from ts_python.granger_causality import granger_causality_calculation
from ts_python.dataset import CSV

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def directory_list(request, files):
    if "delete_file" in request.form:
        files = remove_files(request, files)
    elif "ts_file" in request.form:
        csv = app.config['UPLOAD_FOLDER'] + request.form.get("ts_file")
        session['dataset'] = CSV(csv)
        session['dataset'].show_columns()
    elif "column_button" in request.form:
        column_sample = session['dataset'].show_column_sample(request.form.get("column_button"))
        session["column_samples"] = column_sample
        session["selected_column"] = request.form.get("column_button")


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
    if "submit" in request.form:
        template = "display_ts.html"
        show_image(files, template, form)
    else:
        directory_list(request, files)
    if session.get('ts_columns') is not None:
        form.time_column.choices = session['dataset'].check_time_column()
        form.column_intrest.choices = session['ts_columns']
    return render_template("display_ts.html", files=files, form=form)

@app.route("/calculations", methods=["GET", "POST"])
def calculations():
    form = seasonality_form()
    form2 = trend_form()
    session["non_stationary"]  = "Trend"
    files = get_files(app.config['UPLOAD_FOLDER'])
    if "calculate_trend" in request.form:
        calculate_pvalue_trend(form, form2, files)
    elif "calculate_seasonality" in request.form:
        calculate_pvalue_seasonality(files, form, form2)
    elif "non_stationary" in request.form:
        session["non_stationary"] = request.form.get("non_stationary")
    else:
        directory_list(request, files)
    if session.get('ts_columns') is not None:
        form.time_column.choices = session['dataset'].check_time_column()
        form.column_intrest.choices = session['ts_columns']
        form2.column_intrest.choices = session['ts_columns']
    return render_template("sequencing.html", files=files, form=form, form2=form2)



@app.route("/granger_causality", methods=["GET", "POST"])
def granger_causality():
    files = get_files(app.config['UPLOAD_FOLDER'])
    form = granger_causality_form()
    if "submit" in request.form:
        try:
            if form.column1.data == form.column2.data:
                flash("You have selected the same column", "error")
            dataset = session['dataset'].get_df()
            p_values = granger_causality_calculation(dataset, form.column1.data, form.column2.data, form.lag.data, form.test_function.data)
            session["p_value_granger"] = p_values
        except Exception as e:
            flash(str(e), "error")
    else:
        directory_list(request, files)
    if session.get('ts_columns') is not None:
        form.column1.choices = session['ts_columns']
        form.column2.choices = session['ts_columns']
    return render_template("granger_calculation.html", files=files, form=form)
