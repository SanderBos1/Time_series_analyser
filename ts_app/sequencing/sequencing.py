from flask import Blueprint, session, render_template, flash, current_app, request, jsonify
from ts_app.sequencing.python.trend_calculator import trend_calculator, trend_residuals
from ts_app.sequencing.python.seasonality_calculator import seasonality_calculator
from ts_app.sequencing.python.forms import seasonality_form, trend_form, draw_resiudals
from flask_login import login_required

sequencing_bp = Blueprint('sequencing_bp', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path="/sequencing/static")


@sequencing_bp.route("/trend", methods=["GET", "POST"])
@login_required
def calculations():
    form = trend_form()
    draw_residuals_form = draw_resiudals()
    return render_template("sequencing_trend.html", form=form, draw_residuals_form=draw_residuals_form)


@sequencing_bp.route("/trend/calculate/<dataset>", methods=["POST"])
@login_required
def calculate_trend(dataset):
    form = trend_form()
    form.column_intrest.choices = [form.column_intrest.data]
    if form.validate_on_submit():
        variable_dict = {
            "dataset": current_app.config['UPLOAD_FOLDER']  + dataset,
            "var_column":form.column_intrest.data,
            "trend_function": form.function.data,
        }
        try:
            current_trend_calculator = trend_calculator(variable_dict).calculate_trend()
            if current_trend_calculator > 0.05:
                hypotheses = "H0 is Rejected"
            else:
                hypotheses = "H0 is Accepted"
            values_dict = {
                'p_value':current_trend_calculator,
                'Hypotheses':hypotheses
            }
            return jsonify(values_dict)
        except:
            return "something went wrong"
    return "something went wrong"
    

@sequencing_bp.route("/trend/residuals/<dataset>/<variable>", methods=["POST"])
@login_required
def show_residuals_trend(dataset, variable):
    form = draw_resiudals()
    if form.validate_on_submit():
        plot_variables = {
            "dataset":dataset,
            "variable":variable,
            "xlabel":form.xlabel.data,
            "ylabel":form.ylabel.data,
            "color":form.line_color.data
        }

        img = trend_residuals(plot_variables).show_residuals()
        return img
    return "Something went wrong"


@sequencing_bp.route("/seasonality", methods=["GET", "POST"])
@login_required
def seasonality():
    form = seasonality_form()
    return render_template("sequencing_seasonality.html", form=form)

    

@sequencing_bp.route("/seasonality/calculate/<dataset>", methods=["POST"])
@login_required
def calculate_seasonality(dataset):
    form = seasonality_form()
    form.column_intrest.choices = [form.column_intrest.data]
    if form.validate_on_submit():
        variable_dict = {
            "dataset": current_app.config['UPLOAD_FOLDER']  + dataset,
            "var_column":form.column_intrest.data,
            "seasonality_function": form.function.data,
            "period": form.season_per.data
        }
        try:
            current_seasonality_calculator = seasonality_calculator(variable_dict).calculate_seasonality()
            if current_seasonality_calculator > 0.05:
                hypotheses = "H0 is Rejected"
            else:
                hypotheses = "H0 is Accepted"
            values_dict = {
                'p_value':current_seasonality_calculator,
                'Hypotheses':hypotheses
		    }
            print(values_dict)
            return jsonify(values_dict) 
        except Exception as e:
            print(e)
            return "something went wrong"
    return "something went wrong"
