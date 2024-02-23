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
    """    
    Load the basis of the webpage that handles image logic and display

    """
    form = ts_image_form()
    form_image = image_save_load()
    return render_template("display_ts.html", form = form, form_image = form_image)

@image_ts_bp.route('/display_ts_list', methods=["GET", "POST"])
@login_required
def display_ts_list():
    """    
    Load the basis of the webpage that handles displaying a list of images and the functions on them

    """
    return render_template("display_ts_imagelist.html")


@image_ts_bp.route('/make_image', methods=["POST"])
@login_required
def drawn_image():
    """
    input: 
        form = A user form that indicates which columns are going to be used to draw an image
        it shoud have information for the csv file, 
        which column is the variable and which column is the time variable.
    returns:
        a drawn image displaying a time column on the x axis and a column of interest on the y axis.
    """
    form = ts_image_form()
    form.column_intrest.choices = [form.column_intrest.data]
    form.time_column.choices  =[form.time_column.data]
    if form.validate_on_submit():
        plot_variables = {
            "csv_file": form.dataset.data,
            "time_column":form.time_column.data,
            "var_column":form.column_intrest.data,
            "xlabel": form.xlabel.data,
            "ylabel":form.ylabel.data,
            "color": form.line_color.data
        }
        img = make_image(plot_variables)
        session["ts_image"] = img
        return img
    return "Something has gone wrong"

@image_ts_bp.route('/get_images/', methods=["GET"])
@login_required
def get_images():
    """
    returns a json file containing the name and code of all images in the database
    """
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
    """
    input: The name of the image
    Deletes the image from the database based on its name
    """
    image = ts_image.query.get({image_name})
    db.session.delete(image)
    db.session.commit()
    return "image deleted"


@image_ts_bp.route('/save_image', methods=["POST"])
@login_required
def save_image():
    """
    input: A form containing the name of the image
    saves the images in the database if its name does not already exists
    """
    form_image = image_save_load()
    if form_image.validate_on_submit():
        image_name = form_image.imageName.data
        exists = db.session.query(ts_image.name).filter_by(name=image_name).first() is not None
        if exists:
            return "image already existed"
        image = ts_image(name=image_name, image_code=session["ts_image"])
        db.session.add(image)
        db.session.commit()
        return "Image saved"
    return "Not validated"
