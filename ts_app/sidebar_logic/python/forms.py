from flask_wtf import FlaskForm
from wtforms import MultipleFileField, SubmitField
from flask_wtf.file import FileAllowed, FileRequired


"""
Form to upload a file or files

Has the following attributes:

- file: The file (or files) the user is going to upload
- Submit: A button used to submit the form.
"""


class file_upload_form(FlaskForm):
    file = MultipleFileField(
        label="File", validators=[FileAllowed(["csv"]), FileRequired()]
    )
    submit = SubmitField("Submit")
