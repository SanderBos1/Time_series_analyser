import pandas as pd
from scipy import stats


class seasonality_calculator:
    def __init__(self, file, period, function, time_column, column):
        self.df = pd.read_csv(file)
        self.period = period
        self.function = function
        self.time_column = time_column
        self.column = column

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
    
    def calculate_seasonality(self):
        self.df[self.time_column]= pd.to_datetime(self.df[self.time_column])
        if self.function == "kruskal":
            p_value = self.kruskal_wallis(self.period, self.time_column, self.column)
        print(p_value)
        return round(p_value, 4)
    

