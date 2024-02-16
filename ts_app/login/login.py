import os
from flask import Blueprint, current_app
from flask import render_template, request
from werkzeug.utils import secure_filename

# Defining a blueprint
login_bp = Blueprint('login', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path="/login/static"
                    )
@login_bp.route("/login")
def login():
    return render_template("login.html")

@login_bp.route("/home", methods=["GET", "POST"])
def home_page():
    if  'datasetCSV' in request.form:
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return render_template("home.html")

