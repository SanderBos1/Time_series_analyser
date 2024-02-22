from flask import Blueprint, session, render_template, flash, current_app, request, jsonify
from ts_app.sequencing.python.trend_calculator import trend_calculator
from ts_app.sequencing.python.seasonality_calculator import seasonality_calculator
from ts_app.sequencing.python.forms import seasonality_form, trend_form
from flask_login import login_required

sequencing_bp = Blueprint('sequencing_bp', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path="/sequencing/static")

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
    return render_template("sequencing_trend.html", form=form)


@sequencing_bp.route("/seasonality", methods=["GET", "POST"])
@login_required
def seasonality():
    form = seasonality_form()
    return render_template("sequencing_seasonality.html", form=form)

@sequencing_bp.route("/trend/calculate", methods=["POST"])
@login_required
def calculate_trend():
    form = trend_form()
    form.column_intrest.choices = [form.column_intrest.data]
    if form.validate_on_submit():
        dataset = current_app.config['UPLOAD_FOLDER']  + form.dataset.data
        var_column = form.column_intrest.data
        trend_function = form.function.data
        try:
            current_trend_calculator = trend_calculator(dataset, trend_function, var_column).calculate_trend()
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
    else:
        return "something went wrong"
    

@sequencing_bp.route("/seasonality/calculate", methods=["POST"])
@login_required
def calculate_seasonality():
	form = seasonality_form()
	form.column_intrest.choices = [form.column_intrest.data]
	form.time_column.choices = [form.time_column.data]
	if form.validate_on_submit():
		dataset = current_app.config['UPLOAD_FOLDER']  + form.dataset.data
		var_column = form.column_intrest.data
		tm_column = form.time_column.data
		period = form.season_per.data	
		function = form.function.data
		try:
			current_seasonality_calculator = seasonality_calculator(dataset, period, function, tm_column, var_column).calculate_seasonality()
			if current_seasonality_calculator > 0.05:
				hypotheses = "H0 is Rejected"
			else:
				hypotheses = "H0 is Accepted"
			values_dict = {
				'p_value':current_seasonality_calculator,
				'Hypotheses':hypotheses
			}
			return jsonify(values_dict)
		except:
			return "something went wrong"
	else:
		return "something went wrong"
