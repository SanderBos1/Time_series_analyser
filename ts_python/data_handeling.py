from ts_app import app
from flask import session, render_template, flash, url_for, redirect
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


def show_image(request, file_list, template):
    csvFile = request.form["dataset"] + ".csv"
    period = request.form["period"]
    column = request.form["column"]
    file = app.config['UPLOAD_FOLDER'] + csvFile
    place_image = app.config['IMAGES_FOLDER'] + "tsimage.jpg"
    print(csvFile, period, column, file, place_image)
    try:
        newCSV = CSV(file)
        newCSV.displayCSV(period, column, place_image)
        img = Image.open(place_image)
        data = io.BytesIO()
        img.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        session["ts_image"] = encoded_img_data.decode('utf-8')
        return render_template(template, file_list=file_list)
    except:
        flash("File not found")
        return redirect(url_for(template))