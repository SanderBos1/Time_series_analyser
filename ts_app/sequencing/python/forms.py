from flask_wtf import FlaskForm
from wtforms import StringField, RadioField ,SelectField
from wtforms.validators import InputRequired


class seasonality_form(FlaskForm):
    period_choices = ["Year", "Month"]
    time_column = SelectField(label = "time_column", validators=[InputRequired()])
    column_intrest = SelectField(label = "column_intrest", validators=[InputRequired()])
    period = SelectField(label = "column_intrest", validators=[InputRequired()], choices = period_choices)
    function = RadioField('Label', choices=[('kruskal','kruskal')])

class trend_form(FlaskForm):
    column_intrest = SelectField(label='Time Column', validators=[InputRequired()])
    period = StringField("Period of intrest", validators=[InputRequired()])
    function = RadioField('Label', choices=[('pymannkendall','pymannkendall')])
