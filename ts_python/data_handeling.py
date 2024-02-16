from flask import session, render_template, flash
import base64
import io
from PIL import Image
from ts_app import app
from ts_python.non_stationary_calculator import trend_calculator, seasonality_calculator




def show_image(files, template, form):
    csv_file = session['dataset']
    period = form.time_column.data
    column = form.column_intrest.data
    if period == column:
        flash("You have selected non different columns", "error")
        return render_template(template, files=files, form=form)
    place_image = app.config['IMAGES_FOLDER'] + "tsimage.jpg"
    try:
        csv_file.displayCSV(period, column, place_image)
        img = Image.open(place_image)
        data = io.BytesIO()
        img.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        session["ts_image"] = encoded_img_data.decode('utf-8')
    except Exception as e:
        flash(str(e), "error")
    return render_template(template, files=files, form=form)

def calculate_pvalue_trend(form, form2, files):
    try:
        trend = form2.function.data
        column = form2.column_intrest.data
        file = session['dataset'].get_file()
        new_trend_calculator = trend_calculator(file, trend)
        p_trend = new_trend_calculator.calculate_trend(trend, column)
        session["p_trend"] = p_trend
    except Exception as e:
        flash(str(e), "error")
    return render_template("sequencing.html", files=files, form=form, form2=form2)

def calculate_pvalue_seasonality(files, form, form2):
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
    return render_template("sequencing.html", files=files, form=form, form2=form2)
