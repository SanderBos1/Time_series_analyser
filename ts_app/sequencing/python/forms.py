from flask_wtf import FlaskForm
from wtforms import RadioField ,SelectField, SubmitField, StringField
from wtforms.validators import InputRequired


class seasonality_form(FlaskForm):
    season_per = SelectField(label = "periods", validators=[InputRequired()], choices=[("Year", "Year"), ("Month", "Month")])
    column_intrest = SelectField(label = "column_intrest", validators=[InputRequired()], id="seasonality_column_var")
    function = RadioField(label = 'Statistical Test', choices=[('kruskal','kruskal')], default="kruskal")
    submit = SubmitField("Calculate Seasonality", id="calculate_seasonality")


class trend_form(FlaskForm):
    column_intrest = SelectField(label='Variable of interest', validators=[InputRequired()] , id="trend_column_var")
    function = RadioField(label='Statistical Test', choices=[('pymannkendall','pymannkendall')], default="pymannkendall")
    submit = SubmitField("Calculate Trend", id="calculate_trend")


class stationarity_form(FlaskForm):
    column_intrest = SelectField(label='Variable of interest', validators=[InputRequired()] , id="stationarity_column_var")
    function = RadioField(label='Statistical Test', choices=[('adfuller','adfuller')], default="adfuller")
    submit = SubmitField("Calculate Trend", id="calculate_stationarity")

class make_residuals(FlaskForm):
    column_intrest = SelectField(label='Variable of interest', validators=[InputRequired()] , id="residual_column_intrest")
    function = RadioField(label='Statistical Test', choices=[('detrend','detrend')], default="detrend")
    submit = SubmitField("Make CSV", id="save_residuals_button")