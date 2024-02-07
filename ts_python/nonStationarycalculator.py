import pymannkendall as mk
import pandas as pd
from scipy import stats
import datetime as dt

class trend_calculator:

    def __init__(self, file, trend):
        self.file = file
        self.df = pd.read_csv(self.file)
        self.trend = trend

    def Mann_KendallTrend(self, column):
        p_value = mk.original_test(self.df[column]).p
        return p_value
    
    def calculate_trend(self, trend, column):
        if trend == "pymannkendall":
            trend = self.Mann_KendallTrend(column)
        return round(trend, 4)
    

class seasonality_calculator:
    def __init__(self, file, seasonality):
        self.file = file
        self.df = pd.read_csv(self.file)
        self.seasonality = seasonality

    def kruskal_wallis(self, period, time_column, column):
        res = []
        if period.lower() == "year":
            self.df[period] = self.df[time_column].dt.year
            for i in self.df[time_column].dt.year.unique():
                res.append(self.df[self.df[period] == i][column].values)
        elif period.lower() == "month":
            self.df[period] = self.df[time_column].dt.month
            for i in self.df[time_column].dt.month.unique():
                res.append(self.df[self.df[period] == i][column].values)
        elif period.lower() == "day":
            self.df[period] = self.df[time_column].dt.day
            for i in self.df[time_column].dt.day.unique():
                res.append(self.df[self.df[period] == i][column].values)
        p_value = stats.kruskal(*res).pvalue
        return round(p_value, 4)
    
    def calculate_seasonality(self, period, time_column,  column):
        self.df[time_column]= pd.to_datetime(self.df[time_column])
        if self.seasonality == "kruskal":
            p_value = self.kruskal_wallis(period, time_column, column)
        return round(p_value, 4)
    

