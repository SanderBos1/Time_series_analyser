from flask_wtf import FlaskForm
from wtforms import RadioField ,SelectField, SubmitField, StringField
from wtforms.validators import InputRequired


class seasonality_form(FlaskForm):
    dataset = StringField(label="Dataset", render_kw={'readonly': True}, validators=[InputRequired()])
    period_choices = ["Year", "Month"]
    time_column = SelectField(label = "time_column", validators=[InputRequired()])
    column_intrest = SelectField(label = "column_intrest", validators=[InputRequired()])
    function = RadioField('Label', choices=[('kruskal','kruskal')])
    submit = SubmitField("Show Image", id="calculate_trend")


class trend_form(FlaskForm):
    dataset = StringField(label="Dataset", render_kw={'readonly': True}, validators=[InputRequired()])
    column_intrest = SelectField(label='Time Column', validators=[InputRequired()])
    function = RadioField('Label', choices=[('pymannkendall','pymannkendall')])
    submit = SubmitField("Show Image", id="calculate_trend")
