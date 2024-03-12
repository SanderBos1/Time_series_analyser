import pandas as pd
from matplotlib.figure import Figure
from io import BytesIO
import base64
from flask import current_app
import statsmodels.api as sm

class autocorrelation:
    
    def __init__(self, dataset, column):
        self.column = column
        df = pd.read_csv(current_app.config['UPLOAD_FOLDER'] + dataset)
        df[column] = pd.to_numeric(df[column], errors='coerce')
        self.df = df
        

    def autocorrelation_plot(self):
        """
        Makes an autocorrelation plot of the given dataset and column
        """
        data = self.df[self.column]
        fig = Figure()
        ax = fig.subplots()
        ax.acorr(data, maxlags = 50, color="red")
        ax.set_title("Autocorrelation Plot")
        ax.set_xlabel = "Largs"
        ax.set_ylabel = "correlation"
        buf = BytesIO()
        fig.savefig(buf, format="jpg")
        img_data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return img_data
    
    def partial_autocorrelation(self):
        fig = Figure()
        data = self.df[self.column]
        ax = fig.subplots()
        sm.graphics.tsa.plot_pacf(data, lags=40, method="ywm", ax=ax)
        buf = BytesIO()
        fig.savefig(buf, format="jpg")
        img_data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return img_data

