from flask import Blueprint, flash, jsonify
from flask import render_template, request, url_for, redirect
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from ts_app.login.python.forms import LoginForm, RegistrationForm
from ts_app.models import User
from extensions import db

# Defining the blueprint that handles everything related to logging in.
login_bp = Blueprint(
    "login",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/login/static",
)


@login_bp.route("/", methods=["GET", "POST"])
def login():
    """
    Handles the login process for users.

    If the user is not already logged in,
    this function presents the login page where the user can enter their credentials.
    If the user is already logged in, they are redirected to the homepage. Additionally,
    if the 'register' button is clicked, the user is redirected to the registration page.

    This function checks the user's credentials. If the login attempt is successful,
    the user is logged in and redirected to the homepage.
    If the login attempt fails,
    the user is informed of the invalid username or password and can try again.
    """
    if current_user.is_authenticated:
        return redirect(url_for("login.home_page"))

    form = LoginForm()

    if request.method == "POST" and "register" in request.form:
        return redirect(url_for("login.register"))

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login.login"))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("login.home_page"))

    return render_template("login.html", title="Sign In", form=form)


@login_bp.route("/logout")
def logout():
    """
    Logs out the current user and redirects them to the login page.

    This function calls `logout_user()` to remove the user from the session
    and then redirects the user to the login page, effectively ending their
    current session and requiring them to log in again to access authenticated
    pages.
    """
    logout_user()
    return redirect(url_for("login.login"))


@login_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    loads the registration page
    """

    form = RegistrationForm()
    return render_template("register.html", title="Register", form=form)


@login_bp.route("/register_user", methods=["GET", "POST"])
def registe_userr():
    """
    Displays the registration page and processes registration submissions.

    If the current user is already authenticated, they are redirected to the homepage.
    For new users, this function displays a registration form. Upon submitting the form
    with valid data, it creates a new User record in the database with the provided
    username and email, and hashes the password for secure storage. After successful
    registration, the user is notified and redirected to the login page to sign in with
    their new credentials.
    """
    if current_user.is_authenticated:
        return redirect(url_for("login.home_page"))

    form = RegistrationForm()

    if not form.validate_on_submit():
        return jsonify({"error": "Invalid form submission"}), 400
    try:
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "You have been registered"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    return render_template("register.html", title="Register", form=form)


@login_bp.route("/home", methods=["GET", "POST"])
@login_required
def home_page():
    """
    Renders the home page for authenticated users.
    """
    return render_template("home.html")


@login_bp.route("/settings", methods=["GET", "POST"])
@login_required
def setting_page():
    """
    Renders the setting page.
    """
    return render_template("home.html")
