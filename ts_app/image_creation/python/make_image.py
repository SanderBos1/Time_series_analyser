import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask import current_app
plt.switch_backend('agg')

def make_image(plot_variables):
        df = pd.read_csv(current_app.config['UPLOAD_FOLDER'] + plot_variables["csv_file"])
        df[plot_variables["var_column"]] = pd.to_numeric(df[plot_variables["var_column"]], errors='coerce')
        df[plot_variables["time_column"]] = pd.to_datetime(df[plot_variables["time_column"]])
        plt.plot(df[plot_variables["time_column"]],df[plot_variables["var_column"]], color=plot_variables["color"])
        plt.grid(True)
        plt.title(plot_variables['plot_tile'])
        plt.xlabel(plot_variables["xlabel"])
        plt.xticks(rotation=30, ha='right')
        plt.ylabel(plot_variables["ylabel"])
        img = io.BytesIO()
        plt.savefig(img, format='jpg')
        encoded_img_data = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()
        return encoded_img_data