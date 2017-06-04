"""
Functions to clean WU PWS observation data
"""

import copy
import numpy as np
import pandas as pd
import pickle

def clean_obs_data(df):
    """
    Clean WU PWS data for a single station. Currently just fills missing values w/ NaN's.
    :param df: pandas.DataFrame
        raw data
    :return: cleaned pandas.DataFrame
    """

    df_clean = copy.deepcopy(df)

    # convert strings to numeric where possible
    for col in df_clean.columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='ignore')

    ignore = ["Time", "WindDirection", "SoftwareType", "Conditions", "Clouds", "DateUTC"]

    # low/high limits
    for col in df_clean.columns:
        if col == "TemperatureF":
            df_clean.loc[df_clean[col] <= 10, col] = np.nan
            df_clean.loc[df_clean[col] >= 125, col] = np.nan
        elif col == "DewpointF":
            df_clean.loc[df_clean[col] == -99.9, col] = np.nan
            df_clean.loc[df_clean[col] >= 80, col] = np.nan
            # df_clean.loc[df_clean[col] >= df_clean["TemperatureF"], col] = np.nan
        elif col == "PressureIn":
            df_clean.loc[df_clean[col] <= 25, col] = np.nan
            df_clean.loc[df_clean[col] >= 31.5, col] = np.nan
        elif col == "WindDirectionDegrees":
            df_clean.loc[df_clean[col] < 0, col] = np.nan
            df_clean.loc[df_clean[col] > 360, col] = np.nan
        elif col == "Humidity":
            df_clean.loc[df_clean[col] <= 0, col] = np.nan
            df_clean.loc[df_clean[col] > 100, col] = np.nan
        elif col not in ignore:
            df_clean.loc[df_clean[col] < 0, col] = np.nan

    # TODO: ADD CODE TO AGGREGATE PRECIPITATION DATA!! May write as separate function...?
    # TODO: Add code to convert wind speed/direction into vector for directional averaging?

    # TODO: add checks for outliers based on variance of surrounding data
    # TODO: add checks for frozen values

    return df_clean

def load_weather_data():

    file_list = pd.read_csv('/Users/mgrant/MS_Data_Science/DATA_515/Weather_Project/Project_Git/Ax-Wx/data/weather_file_list.csv')

    data = []
    station = []

    for i in range(1,len(file_list)):
        filename = file_list.ix[i][0]
        station_name = file_list.ix[i][0].split('/')[-1].split('.')[0]
        data = pickle.load(open('%s' % filename, 'rb'))
        data = pd.DataFrame(data)
        data['CumulativePrecip'] = np.cumsum(np.asarray(data['HourlyPrecipIn'], \
        dtype=float))
        clean_data = clean_obs_data(data)
        with open('/Users/mgrant/MS_Data_Science/DATA_515/Weather_Project/Project_Git/Ax-Wx/data/local/cleaned/%s' % station_name + '_cleaned.p','wb') as f:
            pickle.dump(clean_data, f)
