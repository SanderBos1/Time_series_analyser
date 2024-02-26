import pandas as pd
from scipy import stats
from flask import current_app


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
        if self.function == "kruskal":
            p_value = self.kruskal_wallis()
        return round(p_value, 4)
    

