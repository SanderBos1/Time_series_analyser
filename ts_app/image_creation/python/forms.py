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
    dataset = StringField(label="Dataset", render_kw={'readonly': True}, validators=[InputRequired()])
    time_column = SelectField(label='Time Column', validators=[InputRequired()])
    column_intrest = SelectField(label='Column of intrest', validators=[InputRequired()])
    xlabel = StringField(label="X label", validators=[InputRequired()])
    ylabel = StringField(label="Y label", validators=[InputRequired()])
    line_color = SelectField(label='Line Color', validators=[InputRequired()], choices=[("red", "red"), ("blue", "blue")])
    submit = SubmitField("Show Image", id="draw_image_button")