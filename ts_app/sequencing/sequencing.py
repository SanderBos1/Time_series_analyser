from flask import Blueprint, render_template, current_app, jsonify, request
from flask_login import login_required
from ts_app.sequencing.python.decomposition import decomposition_residuals
from ts_app.sequencing.python.stationarity_calculator import trend_calculator, seasonality_calculator, stationarity_calculator
from ts_app.sequencing.python.forms import seasonality_form, trend_form, make_residuals, stationarity_form

sequencing_bp = Blueprint('sequencing_bp', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path="/sequencing/static")


@sequencing_bp.route("/stationary_ptests", methods=["GET", "POST"])
@login_required
def calculations():
    "Loads the trend page and all its HTML elements."
    new_trend_form = trend_form()
    new_seasonality_form = seasonality_form()
    new_stationarity_form = stationarity_form()
    return render_template("stationary_ptests.html", trend_form=new_trend_form, seasonality_form=new_seasonality_form, stationarity_form = new_stationarity_form)


@sequencing_bp.route("/trend/calculate/<dataset>", methods=["POST"])
@login_required
def calculate_trend(dataset):
    """
    Input: 
        Dataset: The file which is used to calculate the trend from
        Column: The column for which trend is calculated
        Trend function: The statistical function that is used
    Results:
        P value + message indicating if Hypotheses 0 can be rejected or not
    """
    form = trend_form()
    form.column_intrest.choices = [form.column_intrest.data]
    current_trend_calculator = "Not defined"
    hypotheses="Not defined"
    try:
        if form.validate():
            variable_dict = {
                "dataset": current_app.config['UPLOAD_FOLDER']  + dataset,
                "var_column":form.column_intrest.data,
                "trend_function": form.function.data,
            }
            current_trend_calculator = trend_calculator(variable_dict).calculate_trend()
            if current_trend_calculator > 0.05:
                hypotheses = "H0 is Accepted, there is no Trend."
            else:
                hypotheses = "H0 is Rejected, there is Trend."
            message="Calculated."
    except Exception as e:
        message = str(e)
    values_dict = {
        "message":message,
        'p_value':current_trend_calculator,
        'Hypotheses':hypotheses
        }
    return values_dict

@sequencing_bp.route("/seasonality/calculate/<dataset>", methods=["POST"])
@login_required
def calculate_seasonality(dataset):
    """
    Input: 
        Dataset: The file which is used to calculate the seasonality farom
        Column: The column for which the hypotheses of seasonality is defined and calculated on
        seasonality function: The statistical function that is used
    Results:
        P value + message indicating if Hypotheses 0 can be rejected or not
    """
    form = seasonality_form()
    form.column_intrest.choices = [form.column_intrest.data]
    current_seasonality_calculator = "Not defined"
    hypotheses="Not defined"
    try:
        if form.validate_on_submit():
            variable_dict = {
                "dataset": current_app.config['UPLOAD_FOLDER']  + dataset,
                "var_column":form.column_intrest.data,
                "seasonality_function": form.function.data,
                "period": form.season_per.data
            }
            current_seasonality_calculator = seasonality_calculator(variable_dict).calculate_seasonality()
            if current_seasonality_calculator > 0.05:
                hypotheses = "H0 is Accepted, there is no Seasonality."
            else:
                hypotheses =  "H0 is Rejected, there is Seasonality."
            message = "Calculated."
    except Exception as e:
        message = str(e)
    values_dict = {
        "message":message,
        'p_value':current_seasonality_calculator,
        'Hypotheses':hypotheses
        }
    return jsonify(values_dict)

@sequencing_bp.route("/stationarity/calculate/<dataset>", methods=["POST"])
@login_required
def stationarity(dataset):
    """
    Input: 
        Dataset: The file which is used to calculate the stationarity form
        Column: The column for which the hypotheses of stationarity is defined and calculated on
        stationarity function: The statistical function that is used
    Results:
        P value + message indicating if Hypotheses 0 can be rejected or not
    """
    form = stationarity_form()
    form.column_intrest.choices = [form.column_intrest.data]
    current_stationarity_calculator = "Not defined"
    hypotheses="Not defined"
    try:
        if form.validate_on_submit():
            variable_dict = {
                "dataset": current_app.config['UPLOAD_FOLDER']  + dataset,
                "var_column":form.column_intrest.data,
                "stationarity_function": form.function.data,
            }
            current_stationarity_calculator = stationarity_calculator(variable_dict).calculate_seasonality()
            if current_stationarity_calculator > 0.05:
                hypotheses = "H0 is Accepted, there is no Stationarity."
            else:
                hypotheses = "H0 is Rejected, there is Stationarity."
            message = "Calculated."
    except Exception as e:
        message = str(e)
    values_dict = {
        "message":message,
        'p_value':current_stationarity_calculator,
        'Hypotheses':hypotheses
        }
    return jsonify(values_dict)

# Decomposition

@sequencing_bp.route("/decomposition", methods=["GET", "POST"])
@login_required
def seasonality():
    "Loads the seasonality page and all its elements."
    make_residuals_form = make_residuals()
    return render_template("residual_logic.html", make_residuals_form=make_residuals_form)

    
@sequencing_bp.route("/add_residuals/<dataset>", methods=["POST"])
@login_required
def add_residuals(dataset):
    """
    Takes a column and makes a csv file of the trend residuals of that column
    """
    form = make_residuals()
    form.column_intrest.choices = [form.column_intrest.data]

    try:
        if form.validate_on_submit:
            variables = {
                "dataset":dataset,
                "variable":form.column_intrest.data,
                "function":form.function.data

            }
            message= decomposition_residuals(variables).add_residuals()
            reaction = "Saved."
    except Exception as e:
        message = str(e)
        reaction = "Something went wrong"
    answer = {
        "answer": reaction,
        "message":message
    }
    return jsonify(answer)
