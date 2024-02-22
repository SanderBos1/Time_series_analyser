from flask import Blueprint, render_template, session, jsonify
from flask_login import login_required
from ..image_creation.python.make_image import make_image
from ..image_creation.python.forms import ts_image_form, image_save_load
from ..image_creation.python.models import ts_image
from ..extensions import db

# Defining a blueprint
image_ts_bp = Blueprint('image', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path="/image/static"
)


@image_ts_bp.route('/display_ts', methods=["GET", "POST"])
@login_required
def display_ts():
    form = ts_image_form()
    form_image = image_save_load()
    return render_template("display_ts.html", form = form, form_image = form_image)

@image_ts_bp.route('/display_ts_list', methods=["GET", "POST"])
@login_required
def display_ts_list():
    return render_template("display_ts_imagelist.html")


@image_ts_bp.route('/make_image', methods=["POST"])
@login_required
def drawn_image():
    """
    input: 
        files = List of csv files in the datadirectory
        form = A user form that indicates which columns are going to be used to draw an image
        form_image = A user form that is used to save the image.

    returns:
        a drawn image displaying a time column on the x axis and a column of interest on the y axis.
    """
    form = ts_image_form()
    form.column_intrest.choices = [form.column_intrest.data]
    form.time_column.choices  =[form.time_column.data]
    if form.validate_on_submit():
        csv_file = form.dataset.data
        period = form.time_column.data
        column = form.column_intrest.data
        img = make_image(csv_file, column, period)
        session["ts_image"] = img
        return img
    else:
        return "Something has gone wrong"

@image_ts_bp.route('/get_images/', methods=["GET"])
@login_required
def get_images():
    images = ts_image.query.all()
    images_converted = {}
    for image in images:
        name = image.get_name()
        image = image.get_image()
        images_converted.update({name : image})
    images_converted = jsonify(images_converted)
    return images_converted

@image_ts_bp.route('/delete/<image_name>', methods=["POST"])
@login_required
def delete_image(image_name):
    image = ts_image.query.get({image_name})
    db.session.delete(image)
    db.session.commit()
    return "image deleted"


@image_ts_bp.route('/save_image', methods=["POST"])
@login_required
def save_image():
		form_image = image_save_load()
		if form_image.validate_on_submit():
			image_name = form_image.imageName.data
			exists = db.session.query(ts_image.name).filter_by(name=image_name).first() is not None
			if exists:
				return "image already existed"
			else:
				image = ts_image(name=image_name, image_code=session["ts_image"])
				db.session.add(image)
				db.session.commit()
				return "Image saved"
		else:
			return "Not validated"





