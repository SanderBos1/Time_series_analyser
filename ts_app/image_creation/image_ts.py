from flask import Blueprint, render_template, session, jsonify, current_app, request
from flask_login import login_required, current_user
from ts_app.image_creation.python.make_image import make_image
from ts_app.image_creation.python.forms import ts_image_form, image_save_load
from ts_app.models import ts_image
from extensions import db


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
    Makes an b64encode encoded image and store it as session variable
    
    Args:
        dataset (str): The filename of the dataset to analyze.

    Returns:
        JSON: {
            "message": A message with the result or error,
            "img": The base64 encoded image
        }
    """
    form = ts_image_form()
    form.column_interest.choices = [form.column_interest.data]
    if not form.validate_on_submit():
        return jsonify({"error": "Invalid form submission"}), 400
    try:
        plot_variables = {
            "csv_file": dataset,
            "time_column": current_app.config['TIME_COLUMN'],
            "var_column":form.column_interest.data,
            "plot_tile": form.image_title.data,
            "xlabel": form.xlabel.data,
            "ylabel":form.ylabel.data,
            "color": form.line_color.data
        }
        img = make_image(plot_variables)
        session["ts_image"] = img
        message="The image is uploaded."
        status_code = 200
    except Exception as e:
        img=""
        message=str(e)
        status_code = 500
    return jsonify({
        "message":message,
        "img": img
    }), status_code

@image_ts_bp.route('/get_images/', methods=["GET"])
@login_required
def get_images():
    
    """
    Gets all images that belong to the logged in user from the database and displays them on the page
    
    Args:
        image_name (str): The filename of thee image to delete

    Returns:
        JSON: {
            "message": A message with the result or error,
            "images": A list containing the name and base64 encoding of the image
        }
    """
    try:
        current_user_name = current_user.username
        images = ts_image.query.filter_by(user = current_user_name )
        images_converted = []
        for image in images:
            name = image.get_name()
            image = image.get_image()
            images_converted.append([name, image])
        message="Images retrieved."
        status_code = 200
    except Exception as e:
        images_converted = []
        message = str(e)
        status_code = 500
    answer = {
        "message":message,
        "images":images_converted
    }

    return jsonify(answer), status_code

@image_ts_bp.route('/delete/<image_name>', methods=["POST"])
@login_required
def delete_image(image_name):

    """
    Deletes the image with the corresponding image_name
    
    Args:
        image_name (str): The filename of thee image to delete

    Returns:
        JSON: {
            "message": A message with the result or error,
        }
    """
    try:
        image = ts_image.query.get({image_name})
        db.session.delete(image)
        db.session.commit()
        message = "Image deleted"
        status_code=200
    except Exception as e:
        message=str(e)
        status_code=500

    answer = {
        "message": message
    }
    return answer, status_code

@image_ts_bp.route('/save_image', methods=["POST"])
@login_required
def save_image():
    """
    Saves the created image to the database
    
    Args:
        Form (form): A form containg the image name

    Returns:
        JSON: {
            "message": A message with the result or error,
        }
    """
    data = request.get_json()
    form = image_save_load.from_json(data["form"])
    try:
        image_user = current_user.username
        if form.validate():
            image_name = form.imageName.data
            image = ts_image(name=image_name, image_code=data["src"], user=image_user)
            db.session.add(image)
            db.session.commit()
            message = "Image is saved."
            status_code=200
    except Exception as e:
        message=str(e)
        status_code=500
    answer = {
        "message":message
    }
    return jsonify(answer), status_code
