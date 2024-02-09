import pandas as pd
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import session
from pandas.api.types import is_datetime64_any_dtype as is_datetime
import numpy as np

#class for csv file handeling
class CSV:
    def __init__(self, file):
        self.file = file
        self.df = pd.read_csv(self.file)
    
    def get_df(self):
        return self.df
    
    def get_file(self):
        return self.file
    
    def get_file_name(self):
        name_file = self.file.split("/")[-1]
        return name_file

    #reads csv files and saves them as an image
    def displayCSV(self, time, column, place):
        self.df[time] = pd.to_datetime(self.df[time])
        plt.plot(self.df[time],self.df[column])
        plt.grid(True)
        plt.title('Time Series - Plot')
        plt.xlabel(time)
        plt.xticks(rotation=30, ha='right')
        plt.ylabel(column)
        plt.savefig(place)
        plt.close()

    def show_columns(self):
        session['ts_columns'] = self.df.columns.tolist()
        return self.df.columns.tolist()
    
    def show_column_sample(self, column):
        df = self.df[column]
        samples = df.sample(n=10, replace=True)
        return samples
    
    def check_time_column(self):
        time_list = self.df.select_dtypes(include=[np.datetime64, "object"]).columns.tolist()
        return time_list


