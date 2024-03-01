from flask_wtf import FlaskForm
from wtforms import MultipleFileField, SubmitField
from flask_wtf.file import FileAllowed, FileRequired

class file_upload_form(FlaskForm):
    file = MultipleFileField(label = 'File', validators=[FileAllowed(['csv']),FileRequired()])
    submit = SubmitField('Submit')