import pymannkendall as mk
import pandas as pd
import matplotlib.pyplot as plt
from flask import current_app
from scipy import stats
from statsmodels.tsa.stattools import adfuller

plt.switch_backend('agg')

class trend_calculator:

    def __init__(self, variable_dict):
        self.df = pd.read_csv(variable_dict["dataset"])
        self.column = variable_dict["var_column"]
        self.trend = variable_dict["trend_function"]

    def Mann_KendallTrend(self):
        p_value = mk.original_test(self.df[self.column]).p
        return p_value
    
    def calculate_trend(self):
        self.df[self.column] = pd.to_numeric(self.df[self.column], errors='coerce')
        if self.trend == "pymannkendall":
            p_value = self.Mann_KendallTrend()
        return round(p_value, 4)
    

class seasonality_calculator:
    def __init__(self, variable_dict):
        self.df = pd.read_csv(variable_dict["dataset"])
        self.column = variable_dict["var_column"]
        self.function = variable_dict["seasonality_function"]
        self.period = variable_dict["period"]
        self.time_column =  current_app.config['TIME_COLUMN']

    def kruskal_wallis(self):
        if self.period.lower() == "year":
            grouped_df = self.df.groupby(pd.Grouper(key=self.time_column, freq='1YE')).mean()
        elif self.period.lower() == "month":
            grouped_df = self.df.groupby(pd.Grouper(key=self.time_column, freq="1M")).mean()
        p_value = stats.kruskal(*grouped_df[self.column].values).pvalue
        return  p_value

    
    def calculate_seasonality(self):
        self.df[self.time_column]= pd.to_datetime(self.df[self.time_column])
        self.df[self.column] = pd.to_numeric(self.df[self.column], errors='coerce')
        if self.function == "kruskal":
            p_value = self.kruskal_wallis()
        return round(p_value, 4)
    


class stationarity_calculator:
    def __init__(self, variable_dict):
        self.df = pd.read_csv(variable_dict["dataset"])
        self.column = variable_dict["var_column"]
        self.function = variable_dict["stationarity_function"]
        self.time_column =  current_app.config['TIME_COLUMN']

    def adfuller(self):
        result = adfuller(self.df[self.column])
        p_value = result[1]
        return  p_value

    
    def calculate_seasonality(self):
        self.df[self.time_column]= pd.to_datetime(self.df[self.time_column])
        self.df[self.column] = pd.to_numeric(self.df[self.column], errors='coerce')
        if self.function == "adfuller":
            p_value = self.adfuller()
        print(p_value)
        return round(p_value, 4)  

    