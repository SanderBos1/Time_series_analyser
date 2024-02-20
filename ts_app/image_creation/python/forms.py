from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,SelectField
from wtforms.validators import InputRequired, DataRequired, Length, Regexp


class image_save_load(FlaskForm):
    imageName = StringField('ImageName',[
        DataRequired(), 
        Length(min=4, max=25), 
        Regexp('^\S+$', message="no white spaces are allowed")
        ])
    save = SubmitField("save Image")

class ts_image_form(FlaskForm):
    time_column = SelectField(label='Time Column', validators=[InputRequired()])
    column_intrest = SelectField(label='Column of intrest', validators=[InputRequired()])
    submit = SubmitField("Show Image")