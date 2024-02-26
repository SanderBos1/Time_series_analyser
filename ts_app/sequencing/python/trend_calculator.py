import pymannkendall as mk
import pandas as pd
from flask import current_app
import matplotlib.pyplot as plt
import io
import base64
plt.switch_backend('agg')

class trend_calculator:

    def __init__(self, variable_dict):
        self.df = pd.read_csv(variable_dict["dataset"])
        self.column = variable_dict["var_column"]
        self.trend = variable_dict["trend_function"]

    def Mann_KendallTrend(self, column):
        p_value = mk.original_test(self.df[column]).p
        return p_value
    
    def calculate_trend(self):
        if self.trend == "pymannkendall":
            p_value = self.Mann_KendallTrend(self.column)
        return round(p_value, 4)
    

class trend_residuals:

    def __init__(self, variables):
        self.variables = variables
    
    def calculate_residuals(self):
        detrend_list = []
        df = pd.read_csv(current_app.config['UPLOAD_FOLDER'] + self.variables["dataset"])
        for i in range(len(df[self.variables["variable"]])-1):
            value = df[self.variables["variable"]][i+1] - df[self.variables["variable"]][i]
            detrend_list.append(value)
        return detrend_list
    
    def show_residuals(self):
        detrend_list = self.calculate_residuals()
        plt.plot(detrend_list,  color=self.variables["color"])
        plt.grid(True)
        plt.title('Time Series - Plot')
        plt.xlabel(self.variables["xlabel"])
        plt.xticks(rotation=30, ha='right')
        plt.ylabel(self.variables["ylabel"])
        img = io.BytesIO()
        plt.savefig(img, format='jpg')
        encoded_img_data = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()
        return encoded_img_data

    