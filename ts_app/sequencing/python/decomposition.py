import pandas as pd
from flask import current_app

class decomposition_residuals:

    def __init__(self, variables):
        self.variables = variables
    
    def calculate_residuals_detrend(self, df):
        detrend_list = []
        for i in range(len(df[self.variables["variable"]])-1):
            value = df[self.variables["variable"]][i+1] - df[self.variables["variable"]][i]
            detrend_list.append(value)
        date_list = df[current_app.config['TIME_COLUMN']]
        date_list = date_list.drop(date_list.index[0])
        time_column = current_app.config['TIME_COLUMN']
        residual_df = pd.DataFrame(
            {  
            time_column: date_list,
            self.variables["variable"]: detrend_list
        })
        name = self.variables["variable"] + "_residuals.csv"
        residual_df.to_csv(current_app.config['UPLOAD_FOLDER'] + name, index=False)
        return "Trend file of " + self.variables["variable"] + " is made."
    
    
    def add_residuals(self):
        df = pd.read_csv(current_app.config['UPLOAD_FOLDER'] + self.variables["dataset"])
        if self.variables['function'] == "detrend":
            message = self.calculate_residuals_detrend(df)
        return message

