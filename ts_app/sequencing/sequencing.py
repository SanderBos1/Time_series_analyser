from flask import Blueprint, session, render_template, flash, current_app, request

from ts_app.sequencing.python.trend_calculator import trend_calculator
from ts_app.sequencing.python.seasonality_calculator import seasonality_calculator
from ts_app.ts_python.buttons_sidebar import directory_list
from ts_app.sequencing.python.forms import seasonality_form, trend_form
from ts_app.ts_python.files import get_files
from flask_login import login_required

sequencing_bp = Blueprint('sequencing_bp', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path="/sequencing/static")


def calculate_pvalue_trend(form, files):
    try:
        trend = form.function.data
        column = form.column_intrest.data
        file = session['dataset'].get_file()
        new_trend_calculator = trend_calculator(file, trend)
        p_trend = new_trend_calculator.calculate_trend(trend, column)
        session["p_trend"] = p_trend
    except Exception as e:
        flash(str(e), "error")
    return render_template("sequencing_trend.html", files=files, form=form)


def calculate_pvalue_seasonality(files, form):
    try:
        seasonality = form.function.data
        time_column = form.time_column.data
        period =  form.period.data
        column = form.column_intrest.data
        file = session['dataset'].get_file()
        new_seasonality_calculator = seasonality_calculator(file, seasonality)
        p_seasonality = new_seasonality_calculator\
            .calculate_seasonality(period, time_column, column)
        session["p_seasonality"] = p_seasonality
    except Exception as e:
        flash(str(e), "error")
    return render_template("sequencing_seasonality.html", files=files, form=form)

@sequencing_bp.route("/trend", methods=["GET", "POST"])
@login_required
def calculations():
    form = trend_form()
    files = get_files(current_app.config['UPLOAD_FOLDER'])
    if "calculate_trend" in request.form:
        calculate_pvalue_trend(form, files)
    else:
        directory_list(request, files)
    if session.get('ts_columns') is not None:
        form.column_intrest.choices = session['ts_columns']
    return render_template("sequencing_trend.html", files=files, form=form)


@sequencing_bp.route("/seasonality", methods=["GET", "POST"])
@login_required
def seasonality():
    form = seasonality_form()
    files = get_files(current_app.config['UPLOAD_FOLDER'])
    if "calculate_seasonality" in request.form:
        calculate_pvalue_seasonality(files, form)
    else:
        directory_list(request, files)
    if session.get('ts_columns') is not None:
        form.time_column.choices = session['dataset'].get_time_columns()
        form.column_intrest.choices = session['ts_columns']
    return render_template("sequencing_seasonality.html", files=files, form=form)
