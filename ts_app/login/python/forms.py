from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from ts_app.models import User
from extensions import db

"""
Form for logging in a user.

Has the following attributes:

- Username: The username of the user. This field is required.
- Password: The corresponding password for the user. This field is required.
- Remember_me: A field that indicates whether the user wants to be remembered for future logins.
- Submit: A button used to submit the form.
"""


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


"""
Form to register a user.

Has the following attributes:

- Username: The username of the user. This field is required.
- Email: The email of the user. This field is required.
- Password: The corresponding password for the user. This field is required.
- Password2: The corresponding password for the user. This field is required and should be the same as the password field.
- Submit: A button used to submit the form.
"""


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        """
        Function that checks if the user name already exist in the database.
        """
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError("Please use a different username.")
