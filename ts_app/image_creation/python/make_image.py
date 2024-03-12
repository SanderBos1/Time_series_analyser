import pandas as pd
from matplotlib.figure import Figure
from io import BytesIO
import base64
from flask import current_app


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
        fig = Figure()
        ax = fig.subplots()
        ax.plot(df[plot_variables["time_column"]],df[plot_variables["var_column"]], color=plot_variables['color'])
        ax.set_title(plot_variables['plot_tile'])
        ax.set_xlabel = plot_variables['xlabel']
        ax.set_ylabel = plot_variables['ylabel']
        buf = BytesIO()
        fig.savefig(buf, format="jpg")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data

