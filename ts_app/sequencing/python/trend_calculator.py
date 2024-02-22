import pymannkendall as mk
import pandas as pd

class trend_calculator:

    def __init__(self, file, trend, column):
        self.df = pd.read_csv(file)
        self.trend = trend
        self.column = column

    def Mann_KendallTrend(self, column):
        p_value = mk.original_test(self.df[column]).p
        return p_value
    
    def calculate_trend(self):
        if self.trend == "pymannkendall":
            p_value = self.Mann_KendallTrend(self.column)
        return round(p_value, 4)
    