from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, IntegerField, SubmitField ,SelectField, PasswordField, BooleanField
from wtforms.validators import ValidationError, InputRequired, DataRequired, Email, EqualTo
from ts_app.extensions import db
import sqlalchemy as sa
from ts_app.image_creation.python.models import User
from email_validator import validate_email

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

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class image_save_load(FlaskForm):
    imageName = StringField('ImageName', validators=[DataRequired()])
    save = SubmitField("save Image")
    


    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

