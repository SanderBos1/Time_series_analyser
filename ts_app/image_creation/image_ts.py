from flask import Blueprint, render_template, session, jsonify, current_app, request
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


@image_ts_bp.route('/make_image/<dataset>', methods=["POST"])
@login_required
def drawn_image(dataset):
    """
    Input: 
        form = A user form that indicates which columns are going to be used to draw an image
        it shoud have information for the csv file, 
        which column is the variable and which column is the time variable.
    Goal: 
        Make an b64encode encoded image and store it as session variable
    Returns:
        a message container an error or a conformation that the image has been uploaded
    """
    form = ts_image_form()
    form.column_intrest.choices = [form.column_intrest.data]
    if form.validate_on_submit():
        try:
            plot_variables = {
                "csv_file": dataset,
                "time_column": current_app.config['TIME_COLUMN'],
                "var_column":form.column_intrest.data,
                "plot_tile": form.image_title.data,
                "xlabel": form.xlabel.data,
                "ylabel":form.ylabel.data,
                "color": form.line_color.data
            }
            img = make_image(plot_variables)
            session["ts_image"] = img
            message="The image is uploaded."
        except Exception as e:
            message=str(e)
    answer = {
        "message":message,
        "img": img
    }
    return jsonify(answer)

@image_ts_bp.route('/get_images/', methods=["GET"])
@login_required
def get_images():
    """
    Input: none
    Goal: show all images from the database
    returns a json file containing the name and code of all images in the database
    """
    try:
        images = ts_image.query.all()
        images_converted = {}
        for image in images:
            name = image.get_name()
            image = image.get_image()
            images_converted.update({name : image})
        message="Images retrieved."
    except Exception as e:
        images_converted = {}
        message = str(e)
    answer = {
        "message":message,
        "images":images_converted
    }
    return jsonify(answer)

@image_ts_bp.route('/delete/<image_name>', methods=["POST"])
@login_required
def delete_image(image_name):
    """
    Input: The name of the image
    Goal: Deletes the image from the database based on its name
    """
    try:
        image = ts_image.query.get({image_name})
        db.session.delete(image)
        db.session.commit()
        message = "Image deleted"
    except Exception as e:
        message=str(e)
    answer = {
        "message": message
    }
    return answer

@image_ts_bp.route('/save_image', methods=["POST"])
@login_required
def save_image():
    """
    Input: A form containing the name of the database
    Goal: to save the drawn image in the database if its name does not already exists
    """
    answer="hello"
    data = request.get_json()
    form = image_save_load.from_json(data["form"])
    try:
        if form.validate():
            image_name = form.imageName.data
            image = ts_image(name=image_name, image_code=data["src"])
            db.session.add(image)
            db.session.commit()
            message = "Image is saved."
    except Exception as e:
        message=str(e)
    answer = {
        "message":message
    }
    return jsonify(answer)
