from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import InputRequired

class ts_image_form(FlaskForm):
    time_column = StringField("Time Colum", validators=[InputRequired()])
    column_intrest = StringField("Column of intrest", validators=[InputRequired()])

class seasonality_form(FlaskForm):
    time_column = StringField("Time Colum", validators=[InputRequired()])
    column_intrest = StringField("Column of intrest", validators=[InputRequired()])
    period = StringField("Period of intrest", validators=[InputRequired()])
    function = RadioField('Label', choices=[('kruskal','kruskal')])

class trend_form(FlaskForm):
    time_column = StringField("Time Colum", validators=[InputRequired()])
    column_intrest = StringField("Column of intrest", validators=[InputRequired()])
    period = StringField("Period of intrest", validators=[InputRequired()])
    function = RadioField('Label', choices=[('pymannkendall','pymannkendall')])



