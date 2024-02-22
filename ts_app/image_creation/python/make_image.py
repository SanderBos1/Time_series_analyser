import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask import current_app
plt.switch_backend('agg')

def make_image(file, var_column, time_column):
    
        df = pd.read_csv(current_app.config['UPLOAD_FOLDER'] + file)
        df[time_column] = pd.to_datetime(df[time_column])
        plt.plot(df[time_column],df[var_column])
        plt.grid(True)
        plt.title('Time Series - Plot')
        plt.xlabel(time_column)
        plt.xticks(rotation=30, ha='right')
        plt.ylabel(var_column)
        img = io.BytesIO()
        plt.savefig(img, format='jpg')
        encoded_img_data = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()
        return encoded_img_data