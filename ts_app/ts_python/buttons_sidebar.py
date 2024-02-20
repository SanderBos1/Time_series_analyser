from flask import session, current_app
from ts_app.ts_python.files import remove_files
from ts_app.ts_python.dataset import CSV

def directory_list(request, files):
    if "delete_file" in request.form:
        files = remove_files(request, files)
    elif "ts_file" in request.form:
        csv = current_app.config['UPLOAD_FOLDER'] + request.form.get("ts_file")
        for key in list(session.keys()):
            session.pop(key)
        session['dataset'] = CSV(csv)
        session['dataset'].show_columns()
    elif "column_button" in request.form:
        column_sample = session['dataset'].show_column_sample(request.form.get("column_button"))
        session["column_samples"] = column_sample
        session["selected_column"] = request.form.get("column_button")