from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os

#defines where the uploaded files are stored and which extensions are allowed
UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = {'csv'}


app = Flask('your_flask_env')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
def hello():
    if  request.method == "POST":
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("home.html")


@app.route('/calculator')
def calculator():
    return render_template("calculator.html")    