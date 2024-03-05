import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask import current_app
plt.switch_backend('agg')

def make_image(plot_variables):
        """
        Generates a plot from a CSV file based on provided plot variables and returns the encoded image data.

        Parameters:
        - plot_variables (dict): A dictionary containing the following keys:
                - "csv_file" (str): The filename of the CSV file containing the data.
                - "var_column" (str): The column name for the variable to be plotted.
                - "time_column" (str): The column name for the time variable.
                - "color" (str): The color of the plot line.
                - "plot_title" (str): The title of the plot.
                - "xlabel" (str): The label for the x-axis.
                - "ylabel" (str): The label for the y-axis.

        Returns:
                - str: The base64-encoded image data of the generated plot.

    """
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