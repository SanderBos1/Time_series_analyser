from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
from pythonFunctions.readCSV import CSV
from pythonFunctions.files import get_files
import base64
import io
from PIL import Image

#defines where the uploaded files are stored and which extensions are allowed
UPLOAD_FOLDER = 'data/'
IMAGES_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = {'csv'}


app = Flask('your_flask_env')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["IMAGES_FOLDER"] = IMAGES_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
def hello():
    if  'datasetCSV' in request.form:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("home.html")


@app.route('/display_ts', methods=["GET", "POST"])
def calculator():
    files = get_files(UPLOAD_FOLDER)
    if "draw" in request.form:
        csvFile = request.form["dataset"]
        period = request.form["period"]
        column = request.form["column"]
        file = UPLOAD_FOLDER + csvFile
        place_image = IMAGES_FOLDER + "tsimage.jpg"
        newCSV = CSV(file)
        newCSV.displayCSV(period, column, place_image)
        img = Image.open(place_image)
        data = io.BytesIO()
        img.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        return render_template("display_ts.html", files=files, img_data = encoded_img_data.decode('utf-8')) 
    if "ts_file" in request.form:
        csv = request.form.get("ts_file")
        file = UPLOAD_FOLDER + csv
        print("this is the value", csv)
        newCSV_columns = CSV(file)
        columns = newCSV_columns.show_columns()
        return render_template("display_ts.html", files=files, columns=columns) 

    return render_template("display_ts.html", files=files)    