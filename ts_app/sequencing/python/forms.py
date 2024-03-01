from flask_wtf import FlaskForm
from wtforms import RadioField ,SelectField, SubmitField, StringField
from wtforms.validators import InputRequired


class seasonality_form(FlaskForm):
    season_per = SelectField(label = "periods", validators=[InputRequired()], choices=[("Year", "Year"), ("Month", "Month")])
    column_intrest = SelectField(label = "column_intrest", validators=[InputRequired()])
    function = RadioField(label = 'Statistical Test', choices=[('kruskal','kruskal')])
    submit = SubmitField("Calculate Seasonality", id="calculate_seasonality")


class trend_form(FlaskForm):
    column_intrest = SelectField(label='Variable of intrest', validators=[InputRequired()])
    function = RadioField(label='Statistical Test', choices=[('pymannkendall','pymannkendall')])
    submit = SubmitField("Calculate Trend", id="calculate_trend")


class draw_resiudals(FlaskForm):
    column_intrest = SelectField(label = "column_intrest", validators=[InputRequired()], id="residual_column_intrest")
    xlabel = StringField(label="X label", validators=[InputRequired()])
    ylabel = StringField(label="Y label", validators=[InputRequired()])
    line_color = SelectField(label='Line Color', validators=[InputRequired()], choices=[("red", "red"), ("blue", "blue")])
    submit = SubmitField("Show plot residuals", id="draw_image_button")