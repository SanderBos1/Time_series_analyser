from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, IntegerField, SubmitField ,SelectField
from wtforms.validators import InputRequired

class ts_image_form(FlaskForm):
    time_column = SelectField(label='Time Column', validators=[InputRequired()])
    column_intrest = SelectField(label='Column of intrest', validators=[InputRequired()])
    submit = SubmitField("Show Image")

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


class granger_causality_form(FlaskForm):
    column1 = SelectField(label = "Column 1", validators=[InputRequired()])
    column2 = SelectField(label = "Column 2", validators=[InputRequired()])
    lag = IntegerField("lag", validators=[InputRequired()])
    test_function = RadioField('test_function', validators=[InputRequired()], choices=[('ssr_ftest','ssr_ftest'), ('ssr_chi2test','ssr_chi2test'), ('lrtest','lrtest')])
    submit = SubmitField("Calculate")


