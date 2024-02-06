from ts_app import app
from flask import session, render_template, flash, url_for, redirect
from ts_python.Trend_calculator import trend_calculator
from ts_python.readCSV import CSV
import base64
import io
from PIL import Image

def show_columns(csv):
    file = app.config['UPLOAD_FOLDER'] + csv
    newCSV_columns = CSV(file)
    columns = newCSV_columns.show_columns()
    session['csv'] = csv.split(".csv")[0]
    session['ts_columns'] = columns


def show_image(request, files, template):
    csvFile = request.form["dataset"] + ".csv"
    period = request.form["period"]
    column = request.form["column"]
    file = app.config['UPLOAD_FOLDER'] + csvFile
    place_image = app.config['IMAGES_FOLDER'] + "tsimage.jpg"
    try:
        newCSV = CSV(file)
        newCSV.displayCSV(period, column, place_image)
        img = Image.open(place_image)
        data = io.BytesIO()
        img.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        session["ts_image"] = encoded_img_data.decode('utf-8')
        min_max_avg = newCSV.show_standard_calculations(column)
        session["min_max_avg"] = min_max_avg
    except Exception as e:
        print(str(e))
        flash(str(e), "error") 
    return render_template(template +".html", files=files)
    
def calculate_pvalue(request, files):
    try:
        trend = request.form.get("trend_function")
        column = request.form["column"]
        file = app.config['UPLOAD_FOLDER'] +  request.form["dataset"] + ".csv"
        new_trend_calculator = trend_calculator(file, trend)
        p_trend = new_trend_calculator.calculate_trend(trend, column)
        session["p_trend"] = p_trend
    except Exception as e:
        flash(str(e), "error") 
    return render_template("sequencing.html", files=files)