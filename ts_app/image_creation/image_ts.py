from flask import Blueprint, flash, render_template, current_app, request, render_template, session
from ts_app.ts_python.files import get_files
from ts_app.ts_python.buttons_sidebar import directory_list
from python_classes.forms import ts_image_form, image_save_load
from flask_login import login_required
from ts_app.image_creation.python.image_functions import save_image

# Defining a blueprint
image_ts_bp = Blueprint('image', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path="/image/static"
)

def show_image(files, template, form):
    csv_file = session['dataset']
    period = form.time_column.data
    column = form.column_intrest.data
    if period == column:
        flash("You have selected non different columns", "error")
        return render_template(template, files=files, form=form)
    try:
        img = csv_file.displayCSV(period, column)
        session["ts_image"] = img
    except Exception as e:
        flash(str(e), "error")
    return render_template(template, files=files, form=form)


@image_ts_bp.route('/display_ts', methods=["GET", "POST"])
@login_required
def display_ts():
    form = ts_image_form()
    form_image = image_save_load()
    files = get_files(current_app.config['UPLOAD_FOLDER'])
    if "submit" in request.form:
        template = "display_ts.html"
        show_image(files, template, form)
    else:
        directory_list(request, files)
    if session.get('dataset') is not None:
        form.time_column.choices = session["dataset"].time_columns
        form.column_intrest.choices = session['ts_columns']
    if "save" in request.form:
        imagename = form_image.imageName.data
        print(imagename)
        save_image(imagename)

    return render_template("display_ts.html", files=files, form=form, form_image = form_image)