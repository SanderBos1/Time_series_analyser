from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, IntegerField, SubmitField 
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


class granger_causality_form(FlaskForm):
    column1 = StringField("Column 1", validators=[InputRequired()])
    column2 = StringField("Column 2", validators=[InputRequired()])
    lag = IntegerField("lag", validators=[InputRequired()])
    test_function = RadioField('test_function', validators=[InputRequired()], choices=[('ssr_ftest','ssr_ftest'), ('ssr_chi2test','ssr_chi2test'), ('lrtest','lrtest')])
    submit = SubmitField("Calculate")


