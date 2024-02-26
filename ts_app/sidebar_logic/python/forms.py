from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired

class file_upload_form(FlaskForm):
    file = FileField(label = 'File', validators=[FileAllowed(['csv']),FileRequired()])
    submit = SubmitField('Submit')