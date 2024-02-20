import os
from flask import Blueprint, current_app, flash
from flask import render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
from ..image_creation.python.models import User
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from ..extensions import db
from python_classes.forms import LoginForm, RegistrationForm
# Defining a blueprint
login_bp = Blueprint('login', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path="/login/static"
                    )

@login_bp.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('login.home_page'))
    form = LoginForm()
    if request.method == "POST":
        if 'register' in request.form:
            return redirect(url_for("login.register"))
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('login.home_page'))
    return render_template('login.html', title='Sign In', form=form)

@login_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login.login'))

@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login.home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login.login'))
    return render_template('register.html', title='Register', form=form)

@login_bp.route("/home", methods=["GET", "POST"])
@login_required
def home_page():
    if  'datasetCSV' in request.form:
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return render_template("home.html")

