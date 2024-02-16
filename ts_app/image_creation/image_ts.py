from flask import Blueprint, flash, render_template, current_app, request, render_template, session
import base64
import io
from PIL import Image

from ts_app.ts_python.files import get_files
from ts_app.ts_python.buttons_sidebar import directory_list
from python_classes.forms import ts_image_form

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
    place_image = current_app.config['IMAGES_FOLDER'] + "tsimage.jpg"
    try:
        csv_file.displayCSV(period, column, place_image)
        img = Image.open(place_image)
        data = io.BytesIO()
        img.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        session["ts_image"] = encoded_img_data.decode('utf-8')
    except Exception as e:
        flash(str(e), "error")
    return render_template(template, files=files, form=form)


@image_ts_bp.route('/display_ts', methods=["GET", "POST"])
def display_ts():
    form = ts_image_form()
    files = get_files(current_app.config['UPLOAD_FOLDER'])
    if "submit" in request.form:
        template = "display_ts.html"
        show_image(files, template, form)
    else:
        directory_list(request, files)
    if session.get('dataset') is not None:
        form.time_column.choices = session["dataset"].time_columns
        print(form.time_column.choices)
        form.column_intrest.choices = session['ts_columns']

    return render_template("display_ts.html", files=files, form=form)