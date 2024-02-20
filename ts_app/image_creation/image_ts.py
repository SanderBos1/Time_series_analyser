from flask import Blueprint, flash, render_template, current_app, request, session
from flask_login import login_required
from ts_app.ts_python.files import get_files
from ts_app.ts_python.buttons_sidebar import directory_list
from ..image_creation.python.forms import ts_image_form, image_save_load
from ..image_creation.python.models import ts_image
from ..extensions import db

# Defining a blueprint
image_ts_bp = Blueprint('image', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path="/image/static"
)

def show_image(files, form, form_image):
    """
    input: 
        files = List of csv files in the datadirectory
        form = A user form that indicates which columns are going to be used to draw an image
        form_image = A user form that is used to save the image.

    returns:
        a drawn image displaying a time column on the x axis and a column of interest on the y axis.
    """
    csv_file = session['dataset']
    period = form.time_column.data
    column = form.column_intrest.data
    if period == column:
        flash("You have selected non different columns", "error")
        return render_template("display_ts_imagelist.html", files=files, form=form)
    img = csv_file.displayCSV(period, column)
    session["ts_image"] = img
    return render_template("display_ts_imagelist.html", files=files, form=form, \
                            form_image = form_image)

@image_ts_bp.route('/display_ts', methods=["GET", "POST"])
@login_required
def display_ts():
    form = ts_image_form()
    form_image = image_save_load()
    files = get_files(current_app.config['UPLOAD_FOLDER'])
    if "submit" in request.form:
        show_image(files, form, form_image)
    if session.get('dataset') is not None:
        form.time_column.choices = session["dataset"].time_columns
        form.column_intrest.choices = session['ts_columns']
    if "save" in request.form:
        if form_image.validate_on_submit():
            image_name = form_image.imageName.data
            image = ts_image(name=image_name, image_code =session["ts_image"])
            db.session.add(image)
            db.session.commit()
    else:
        directory_list(request, files)
    return render_template("display_ts.html", files=files, form=form, form_image = form_image)

@image_ts_bp.route('/display_ts_list', methods=["GET", "POST"])
@login_required
def display_ts_list():
    images = ts_image.query.all()
    files = get_files(current_app.config['UPLOAD_FOLDER'])
    if "delete_image" in request.form:
        image_id = request.form["delete_image"]
        image = ts_image.query.get(image_id)
        db.session.delete(image)
        db.session.commit()
        images = ts_image.query.all()
    else:
        directory_list(request, files)
    return render_template("display_ts_imagelist.html", images=images, files=files)
