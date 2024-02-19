from flask import session, current_app
import os
import io
import base64
from PIL import Image

def save_image(imagename):
    imgData = base64.b64decode(str(session["ts_image"]))
    img = Image.open(io.BytesIO(imgData))
    img.save(os.path.join(current_app.config['USER_IMAGE_FOLDER'], imagename + ".jpg"))

