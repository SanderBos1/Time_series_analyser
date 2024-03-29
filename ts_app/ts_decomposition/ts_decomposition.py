from flask import Blueprint, render_template, current_app, jsonify
from flask_login import login_required
from ts_app.image_creation.python.make_image import make_image
from ts_app.ts_decomposition.python.autocorrelation import explore_ts
from ts_app.ts_decomposition.python.decomposition import decomposition_residuals
from ts_app.ts_decomposition.python.stattest_calculator import (
    trend_calculator,
    seasonality_calculator,
    stationarity_calculator,
)
from ts_app.ts_decomposition.python.forms import (
    seasonality_form,
    trend_form,
    make_residuals,
    stationarity_form,
)

# Blueprint for the  section that handles decomposition of time-series logic inside the application
ts_decomposition_bp = Blueprint(
    "ts_decomposition_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/ts_decomposition/static",
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

    return render_template(
        "exploratory_analysis.html",
        trend_form=new_trend_form,
        seasonality_form=new_seasonality_form,
        stationarity_form=new_stationarity_form,
    )


@ts_decomposition_bp.route("/trend/calculate/<dataset>/<column>", methods=["POST"])
@login_required
def calculate_trend(dataset, column):
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
    if not form.validate_on_submit():
        return jsonify({"error": "Invalid form submission"}), 400
    try:
        variable_dict = {
            "dataset": current_app.config["UPLOAD_FOLDER"] + dataset,
            "var_column": column,
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

    return (
        jsonify({"message": message, "p_value": p_value, "Hypotheses": hypotheses}),
        status_code,
    )


@ts_decomposition_bp.route(
    "/seasonality/calculate/<dataset>/<column>", methods=["POST"]
)
@login_required
def calculate_seasonality(dataset, column):
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
    if not form.validate_on_submit():
        return jsonify({"error": "Invalid form submission"}), 400
    try:
        variable_dict = {
            "dataset": current_app.config["UPLOAD_FOLDER"] + dataset,
            "var_column": column,
            "seasonality_function": form.function.data,
            "period": form.season_per.data,
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
    return (
        jsonify({"message": message, "p_value": p_value, "Hypotheses": hypotheses}),
        status_code,
    )


@ts_decomposition_bp.route(
    "/stationarity/calculate/<dataset>/<column>", methods=["POST"]
)
@login_required
def calculate_stationarity(dataset, column):
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
    if not form.validate_on_submit():
        return jsonify({"error": "Invalid form submission"}), 400
    try:
        variable_dict = {
            "dataset": current_app.config["UPLOAD_FOLDER"] + dataset,
            "var_column": column,
            "stationarity_function": form.function.data,
        }
        p_value = stationarity_calculator(variable_dict).calculate_seasonality()
        if p_value <= 0.05:
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

    return (
        jsonify({"message": message, "p_value": p_value, "Hypotheses": hypotheses}),
        status_code,
    )


@ts_decomposition_bp.route("/autocorrelation/<dataset>/<column>", methods=["POST"])
@login_required
def display_autocorrelation(dataset, column):
    """
    Makes autocorrelation plot on column click.

    Args:
        dataset (str): The filename of the dataset to analyze.
        column (str): The column for which autocorrelations are calculated


    Returns:
            JSON: {
            "message": A message with the result or error,
            "img_auto": The autocorrelation plot image
            "img_partial": The partial autocorrelation plot image
            "ts_img": The plot of the time-series
        }

    """
    try:
        autocorrelation_plotter = explore_ts(dataset, column)
        img_autocorrelation = autocorrelation_plotter.autocorrelation_plot()
        img_partial_autocorrelation = autocorrelation_plotter.partial_autocorrelation()
        plot_variables = {
            "csv_file": dataset,
            "time_column": current_app.config["TIME_COLUMN"],
            "var_column": column,
            "plot_tile": "time-series of " + column,
            "xlabel": "Date",
            "ylabel": column,
            "color": "red",
        }
        ts_img = make_image(plot_variables)
        stats = autocorrelation_plotter.stat_descriptors()
        status_code = 200
        return (
            jsonify(
                {
                    "Img_auto": img_autocorrelation,
                    "Img_partial": img_partial_autocorrelation,
                    "ts_img": ts_img,
                    "stats": stats,
                }
            ),
            status_code,
        )
    except Exception as e:
        status_code = 500
        return jsonify({"Error": str(e)}), status_code



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


@ts_decomposition_bp.route("/add_residuals/<dataset>/<column>", methods=["POST"])
@login_required
def add_residuals(dataset, column):
    """
    Takes a column and makes a csv file of the  residuals of that column using a function that makes the column stationary
    """
    form = make_residuals()
    try:
        if form.validate_on_submit():
            variables = {
                "dataset": dataset,
                "variable": column,
                "function": form.function.data,
            }

            plot_variables = {
                "csv_file": dataset,
                "time_column": current_app.config["TIME_COLUMN"],
                "var_column": column,
                "plot_tile": "time-series of " + column,
                "xlabel": "Date",
                "ylabel": column,
                "color": "red",
            }

            ts_img = make_image(plot_variables)

            name = decomposition_residuals(variables).add_residuals()
            plot_variables_after = {
                "csv_file": name,
                "time_column": current_app.config["TIME_COLUMN"],
                "var_column": column,
                "plot_tile": "time-series of " + column + "after" + form.function.data,
                "xlabel": "Date",
                "ylabel": column,
                "color": "red",
            }
            ts_img_after = make_image(plot_variables_after)

            response = {
                "message": "Residuals added successfully.",
                "ts_img": ts_img,
                "ts_img_after": ts_img_after,
            }
            status_code = 200

        else:
            response = {"message": "Invalid form submission."}
            status_code = 200
    except Exception as e:
        response = {"success": False, "message": str(e)}
        status_code = 500
    return jsonify(response), status_code
