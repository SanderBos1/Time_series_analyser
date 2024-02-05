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
        self.df[time] = pd.to_datetime(self.df[time])
        plt.plot(self.df[time],self.df[column])
        plt.title('Time Series - Plot')
        plt.xlabel("Date")
        plt.xticks(rotation=30, ha='right')
        plt.ylabel(column)
        plt.savefig(place)

    def show_columns(self):
        return self.df.columns.tolist()



#csv = CSV("data/Electric_Production.csv")
#csv.displayCSV("DATE", "IPG2211A2N", "static/images/test.jpg")