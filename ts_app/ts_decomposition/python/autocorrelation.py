import pandas as pd
import matplotlib.pyplot as plt 
import statsmodels.api as sm
import io
import base64
from flask import current_app
plt.switch_backend('agg')

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
        plt.title("Autocorrelation Plot" + self.column)
        plt.xlabel = "Largs"
        plt.acorr(data, maxlags = 50) 
        plt.grid(True)
        img = io.BytesIO()
        plt.savefig(img, format='jpg')
        encoded_img_data = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()
        return encoded_img_data

    def partial_autocorrelation(self):
        data = self.df[self.column]
        sm.graphics.tsa.plot_pacf(data, lags=40, method="ywm")
        partial = io.BytesIO()
        plt.savefig(partial, format='jpg')
        partial_img_data = base64.b64encode(partial.getvalue()).decode('utf-8')
        plt.close()
        return partial_img_data