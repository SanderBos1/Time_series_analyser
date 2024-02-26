from flask import Blueprint, current_app, session, jsonify, request, g
from werkzeug.utils import secure_filename
from flask_login import login_required
import os
import glob
import pandas as pd
from ..sidebar_logic.python.forms import file_upload_form

sidebar_bp = Blueprint('sidebar_bp', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path="/sidebar_logic/static"
)

@sidebar_bp.app_context_processor
def inject_file_form():
    return dict(upload_form=file_upload_form())


@sidebar_bp.route('/columns/<name>', methods=["GET"])
@login_required
def select_dataset(name):
    csv = current_app.config['UPLOAD_FOLDER'] + name
    df = pd.read_csv(csv)
    columns = df.columns.tolist()
    column_dictionary = {}
    for i in range(len(columns)):
        column_dictionary.update({i : columns[i]})
    return jsonify(column_dictionary)

@sidebar_bp.route('/get_csvfiles', methods=["GET"])
@login_required
def get_datasets():
    csvFiles = [os.path.basename(x) for x in glob.glob(current_app.config['UPLOAD_FOLDER'] + '/*.csv')]
    file_dict = {}
    for number in range(len(csvFiles)):
        file_dict.update({number : csvFiles[number]})
    return jsonify(file_dict)


@sidebar_bp.route('/delete_csv/<name>', methods=["POST"])
@login_required
def delete_dataset(name):
    csv =name
    remove_file = current_app.config['UPLOAD_FOLDER'] + csv
    os.remove(remove_file)
    return csv + "deleted"


@sidebar_bp.route("/upload", methods=["POST"])
@login_required
def upload_csv_data():
    print("test")
    form = file_upload_form()
    if form.validate_on_submit():
        filename = form.file.data.filename
        form.file.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return "File is not uploaded"
