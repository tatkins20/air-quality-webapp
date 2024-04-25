import streamlit as st
import requests
import json
import pandas as pd
import pytz
import os
import plotly.express as px

# Extract
def get_api_key():
    """
    Function to retrieve API keys from Streamlit secrets.

    Returns:
        tuple: A tuple containing API key and Mapbox key.
    """
    key = st.secrets['appid']
    mapboxkey = st.secrets['mapboxkey']
    return key, mapboxkey

def extract_current(key, latitude, longitude):
    """
    Function to extract current air pollution data from the API.

    Args:
        key (str): API key.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.

    Returns:
        dict: Response JSON containing current air pollution data.
    """
    getUrl = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}'
    response = requests.get(getUrl, params={"appid": key})
    return response.json()

def extract_forecast(key, latitude, longitude):
    """
    Function to extract forecast air pollution data from the API.

    Args:
        key (str): API key.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.

    Returns:
        dict: Response JSON containing forecast air pollution data.
    """
    getUrl = f'https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={latitude}&lon={longitude}'
    response = requests.get(getUrl, params={"appid": key})
    return response.json()

# Transform
def transform_response(response):
    """
    Function to transform JSON response into a pandas DataFrame.

    Args:
        response (dict): JSON response.

    Returns:
        DataFrame: Transformed DataFrame.
    """
    data = response['list']
    df = pd.json_normalize(data)
    return df

# The App in action
def main():
    st.title("Air Pollution Data Visualization")

    # Input latitude and longitude
    latitude = st.number_input('Enter Latitude:')
    longitude = st.number_input('Enter Longitude:')

    if latitude and longitude:  # Check if latitude and longitude are provided
        # Process
        key, mapboxkey = get_api_key()
        response_current = extract_current(key, latitude, longitude)
        response_forecast = extract_forecast(key, latitude, longitude)
        df_current = transform_response(response_current)
        df_forecast = transform_response(response_forecast)

        # Visualize with Plotly and Mapbox
        st.title('Current Air Pollution Data')
        fig_current = px.scatter_mapbox(df_current, lat='coord.lat', lon='coord.lon', hover_name='dt', hover_data=['main.aqi', 'components'], 
                                         color='main.aqi', color_continuous_scale=px.colors.cyclical.IceFire, size='main.aqi', size_max=15, zoom=10)
        fig_current.update_layout(mapbox_style='open-street-map', mapbox_accesstoken=mapboxkey)
        st.plotly_chart(fig_current)

        st.title('Forecasted Air Pollution Data')
        fig_forecast = px.line(df_forecast, x='dt', y='main.aqi', title='Air Quality Index Forecast', labels={'main.aqi': 'Air Quality Index'})
        st.plotly_chart(fig_forecast)
    else:
        st.write('Please enter latitude and longitude to view air pollution data.')

if __name__ == "__main__":
    main()
