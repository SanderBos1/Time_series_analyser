from flask import Blueprint, render_template, current_app, jsonify
from flask_login import login_required
from ts_app.ts_decomposition.python.decomposition import decomposition_residuals
from ts_app.ts_decomposition.python.stationarity_calculator import trend_calculator, seasonality_calculator, stationarity_calculator
from ts_app.ts_decomposition.python.forms import seasonality_form, trend_form, make_residuals, stationarity_form

# Blueprint for the  section that handles decomposition of time-series logic inside the application
ts_decomposition_bp = Blueprint(
    'ts_decomposition_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path="/ts_decomposition/static"
)


@ts_decomposition_bp.route("/stationary_ptests", methods=["GET", "POST"])
@login_required
def show_stationary_tests():
    """
    Handles the loading of the page that allows users to perform stationary statistical tests.

    This page enables users to input data and parameters for trend analysis, seasonality checks,
    and stationarity tests. Each form corresponds to a different aspect of time-series decomposition analysis.
    """
    new_trend_form = trend_form()
    new_seasonality_form = seasonality_form()
    new_stationarity_form = stationarity_form()

    return render_template("stationary_ptests.html", 
                           trend_form=new_trend_form, 
                           seasonality_form=new_seasonality_form, 
                           stationarity_form=new_stationarity_form)

@ts_decomposition_bp.route("/trend/calculate/<dataset>", methods=["POST"])
@login_required
def calculate_trend(dataset):
    """
    Calculates and returns the trend of a specified column in a dataset using a selected statistical function.
    
    Args:
        dataset (str): The filename of the dataset to analyze.
    
    Returns:
        JSON: {
            "message": A message with the result or error,
            "p_value": The calculated p-value,
            "hypotheses": The interpretation of the hypotheses test
        }
    """
    form = trend_form()
    form.column_interest.choices = [form.column_interest.data]    
    if not form.validate_on_submit():
        return jsonify({"error": "Invalid form submission"}), 400
    try:
        variable_dict = {
            "dataset": current_app.config['UPLOAD_FOLDER'] + dataset,
            "var_column": form.column_interest.data,  
            "trend_function": form.function.data,
        }
        p_value = trend_calculator(variable_dict).calculate_trend()
        if p_value <= 0.05:
            hypotheses = "H0 is Rejected, there is Trend."
        else: 
            hypotheses = "H0 is Accepted, there is no Trend."
        message = "Calculation successful."
        status_code = 200
    except Exception as e:
        message = f"Error during calculation: {str(e)}"
        p_value = None
        hypotheses = "Calculation error"
        status_code = 500

    return jsonify({
        "message": message,
        'p_value': p_value,
        'Hypotheses': hypotheses
    }), status_code

@ts_decomposition_bp.route("/seasonality/calculate/<dataset>", methods=["POST"])
@login_required
def calculate_seasonality(dataset):
    """
    Calculates and returns the seasonality of a specified column in a dataset using a selected statistical function.
    
    Args:
        dataset (str): The filename of the dataset to analyze.
    
    Returns:
        JSON: {
            "message": A message with the result or error,
            "p_value": The calculated p-value,
            "hypotheses": The interpretation of the hypotheses test
        }
    """
    form = seasonality_form()
    form.column_interest.choices = [form.column_interest.data]
    if not form.validate_on_submit():
        return jsonify({"error": "Invalid form submission"}), 400
    try:
        variable_dict = {
            "dataset": current_app.config['UPLOAD_FOLDER']  + dataset,
            "var_column":form.column_interest.data,
            "seasonality_function": form.function.data,
            "period": form.season_per.data
        }
        p_value = seasonality_calculator(variable_dict).calculate_seasonality()
        if p_value <= 0.05:
            hypotheses = "H0 is Rejected, there is seasonality."
        else: 
            hypotheses = "H0 is Accepted, there is no seasonality."
        message = "Calculation successful."
        status_code = 200
    except Exception as e:
        message = f"Error during calculation: {str(e)}"
        p_value = None
        hypotheses = "Calculation error"
        status_code = 500
    return jsonify({
        "message": message,
        'p_value': p_value,
        'Hypotheses': hypotheses
    }), status_code

@ts_decomposition_bp.route("/stationarity/calculate/<dataset>", methods=["POST"])
@login_required
def calculate_stationarity(dataset):
    """
    Calculates and returns the stationarity of a specified column in a dataset using a selected stationarity function.
    
    Args:
        dataset (str): The filename of the dataset to analyze.
    
    Returns:
        JSON: {
            "message": A message with the result or error,
            "p_value": The calculated p-value,
            "hypotheses": The interpretation of the hypotheses test
        }
    """
    form = stationarity_form()
    form.column_interest.choices = [form.column_interest.data]
    if not form.validate_on_submit():
        return jsonify({"error": "Invalid form submission"}), 400
    try:
        variable_dict = {
            "dataset": current_app.config['UPLOAD_FOLDER']  + dataset,
            "var_column":form.column_interest.data,
            "stationarity_function": form.function.data,
        }
        p_value = stationarity_calculator(variable_dict).calculate_seasonality()
        if p_value  <= 0.05:
            hypotheses = "H0 is Rejected, there is stationarity."
        else: 
            hypotheses = "H0 is Accepted, there is no stationarity."
        message = "Calculation successful."
        status_code = 200
    except Exception as e:
        message = f"Error during calculation: {str(e)}"
        p_value = None
        hypotheses = "Calculation error"
        status_code = 500

    return jsonify({
        "message": message,
        'p_value': p_value,
        'Hypotheses': hypotheses
    }), status_code

# Decomposition

@ts_decomposition_bp.route("/decomposition", methods=["GET", "POST"])
@login_required
def load_decomposition():
    """
    Loads the decomposition page and its elements including form(s) for making residuals.
    """
    # Create form for making residuals
    residuals_form = make_residuals()
    
    return render_template("residual_logic.html", residuals_form=residuals_form)

    
@ts_decomposition_bp.route("/add_residuals/<dataset>", methods=["POST"])
@login_required
def add_residuals(dataset):
    """
    Takes a column and makes a csv file of the  residuals of that column using a function that makes the column stationary
    """
    form = make_residuals()
    form.column_interest.choices = [form.column_interest.data]
    try:
        if form.validate_on_submit():
            variables = {
                "dataset": dataset,
                "variable": form.column_interest.data,  # Assuming typo correction
                "function": form.function.data
            }
            message = decomposition_residuals(variables).add_residuals()
            response = {"message": "Residuals added successfully."}
            status_code = 200

        else:
            response = {"message": "Invalid form submission."}
            status_code = 200
    except Exception as e:
        response = {"success": False, "message": str(e)}
        status_code = 500
    return jsonify(response), status_code