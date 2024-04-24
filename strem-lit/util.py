from dotenv import load_dotenv
import os
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
import pickle
from matplotlib import pyplot as plt
import numpy as np


load_dotenv()
data_fol = Path(os.getenv("DATA_FOL"))
v1 = data_fol / 'v1'
tn_v1 = data_fol / 'tn_v1'

def load_pickle(file):
    return pickle.load(open(file, 'rb'))

temp = load_pickle(data_fol/'weather.pkl')
rainfall = load_pickle(data_fol/'rainfall.pkl')



def apply_temp_rainfall(row):
    
    date = row['date'].date()
    cur_temp = temp.get(date, (None, None))

    row['tmin'] = cur_temp[0]
    row['tmax'] = cur_temp[1]
    row['rainfall'] = rainfall.get(str(date), None)

    return row


def open_file(file_name):

    df = pd.read_feather(file_name)
    df = df.apply(apply_temp_rainfall, axis=1)
    df = df.dropna()
    df = df.set_index('date')
    df = df.drop(['min', 'max'], axis=1)
    df = df.rename(columns={'modal': 'price'})

    # time series features
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear

    return df


def forecast(df, forecast_week):

    average = df['price'].mean()
    std_dev = df['price'].diff().std()
    percentage = std_dev/average

    last_price = df['price'].iloc[-1]
    descent_percentages = np.random.uniform(low=(-percentage/10), high=percentage, size=forecast_week)
    descent_percentages[0] = 0

    dates = pd.date_range(start=df.index[-1], periods=forecast_week, freq='1W')
    forecast_prices = last_price * (1 + descent_percentages)

    forecast_df = pd.DataFrame({'forcasted': forecast_prices}, index=dates)

    return forecast_df


def get_weather_info():
    df = pd.DataFrame(pd.date_range(start='2015-01-01', end='2024-04-01'), columns=['date'])
    df = df.apply(apply_temp_rainfall, axis=1)
    df = df.set_index('date')

    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear

    return df