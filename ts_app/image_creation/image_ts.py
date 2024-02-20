from flask import Blueprint, flash, render_template, current_app, request, render_template, session
from ts_app.ts_python.files import get_files
from ts_app.ts_python.buttons_sidebar import directory_list
from python_classes.forms import ts_image_form, image_save_load
from flask_login import login_required
from ts_app.image_creation.python.image_functions import save_image
from ..image_creation.python.models import ts_image
from ..extensions import db

# Defining a blueprint
image_ts_bp = Blueprint('image', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path="/image/static"
)

def show_image(files, template, form, form_image):
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
    return render_template(template, files=files, form=form,  form_image = form_image)


@image_ts_bp.route('/display_ts', methods=["GET", "POST"])
@login_required
def display_ts():
    form = ts_image_form()
    form_image = image_save_load()
    files = get_files(current_app.config['UPLOAD_FOLDER'])
    if "submit" in request.form:
        template = "display_ts.html"
        show_image(files, template, form, form_image)
    else:
        directory_list(request, files)
    if session.get('dataset') is not None:
        form.time_column.choices = session["dataset"].time_columns
        form.column_intrest.choices = session['ts_columns']
    if "save" in request.form:
        imagename = form_image.imageName.data
        Image = ts_image(name =imagename, image_code =session["ts_image"])
        db.session.add(Image)
        db.session.commit()
    return render_template("display_ts.html", files=files, form=form, form_image = form_image)

@image_ts_bp.route('/display_ts_list', methods=["GET", "POST"])
@login_required
def display_ts_list():
    images = ts_image.query.all()
    files = get_files(current_app.config['UPLOAD_FOLDER'])
    if "delete_image" in request.form:
        print(request.form["delete_image"])
        id = request.form["delete_image"]
        Image = ts_image.query.get(id)
        db.session.delete(Image)
        db.session.commit()
        images = ts_image.query.all()
    else:
        directory_list(request, files)
    return render_template("display_ts_imagelist.html", images=images, files=files)


