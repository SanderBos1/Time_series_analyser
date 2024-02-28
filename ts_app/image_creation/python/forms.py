from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField ,SelectField
from wtforms.validators import InputRequired, DataRequired, Length, Regexp


class image_save_load(Form):
    imageName = StringField('ImageName',[
        DataRequired(), 
        Length(min=4, max=25), 
        Regexp('^\S+$', message="no white spaces are allowed")
        ])
    save = SubmitField("save Image")

class ts_image_form(FlaskForm):
    column_intrest = SelectField(label='Column of intrest', validators=[InputRequired()])
    xlabel = StringField(label="X label", validators=[InputRequired()])
    ylabel = StringField(label="Y label", validators=[InputRequired()])
    line_color = SelectField(label='Line Color', validators=[InputRequired()], choices=[("red", "red"), ("blue", "blue")])
    submit = SubmitField("Show Image", id="draw_image_button")