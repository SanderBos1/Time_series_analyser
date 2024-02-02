import pandas as pd
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt


#class for csv file handeling
class CSV:
    def __init__(self, file):
        self.file = file
        self.df = pd.read_csv(self.file)

    #reads csv files and saves them as an image
    def displayCSV(self, time, column, place):
        plt.plot(self.df[time],self.df[column] )
        plt.savefig(place)

    def show_columns(self):
        print(self.df.columns.tolist())
        return self.df.columns.tolist()

