from flask_wtf import FlaskForm
from wtforms import RadioField, IntegerField, SubmitField ,SelectField
from wtforms.validators import  InputRequired

class granger_causality_form(FlaskForm):
    column1 = SelectField(label = "Column 1", validators=[InputRequired()])
    column2 = SelectField(label = "Column 2", validators=[InputRequired()])
    lag = IntegerField("lag", validators=[InputRequired()])
    test_function = RadioField('test_function', validators=[InputRequired()], choices=[('ssr_ftest','ssr_ftest'), ('ssr_chi2test','ssr_chi2test'), ('lrtest','lrtest')])
    submit = SubmitField("Calculate")
