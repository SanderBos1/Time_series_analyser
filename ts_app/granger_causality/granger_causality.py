from flask import request, render_template, session, flash, current_app, Blueprint
from ts_app.granger_causality.python.granger_causality import granger_causality_calculation
from ts_app.granger_causality.python.forms import granger_causality_form
from ts_app.ts_python.buttons_sidebar import directory_list
from ts_app.ts_python.files import get_files
from flask_login import login_required

granger_bp = Blueprint('granger_bp', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path="/granger/static")

@granger_bp.route("/granger_causality", methods=["GET", "POST"])
@login_required
def granger_causality():
    files = get_files(current_app.config['UPLOAD_FOLDER'])
    form = granger_causality_form()
    if "submit" in request.form:
        try:
            if form.column1.data == form.column2.data:
                flash("You have selected the same column", "error")
            dataset = session['dataset'].get_df()
            p_values = granger_causality_calculation(dataset, form.column1.data, form.column2.data, form.lag.data, form.test_function.data)
            session["p_value_granger"] = p_values
        except Exception as e:
            flash(str(e), "error")
    else:
        directory_list(request, files)
    if session.get('ts_columns') is not None:
        form.column1.choices = session['ts_columns']
        form.column2.choices = session['ts_columns']
    return render_template("granger_calculation.html", files=files, form=form)
