import pymannkendall as mk
import pandas as pd

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
        return trend
