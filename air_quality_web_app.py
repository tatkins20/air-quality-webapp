import streamlit as st
import requests
import json
import pandas as pd
import pytz
import os
import plotly.express as px

# Extract
def get_api_key():
    key = os.environ.get('OPENWEATHER_API_KEY')
    mapbox_key = os.environ.get('MAPBOX_API_KEY')
    if key is None or mapbox_key is None:
        st.error("Please set the OPENWEATHER_API_KEY and MAPBOX_API_KEY environment variables.")
        st.stop()
    return key, mapbox_key

def extract_current(latitude, longitude, api_key):
    url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}'
    response = requests.get(url)
    return response.json()

def extract_forecast(latitude, longitude, api_key):
    url = f'https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={latitude}&lon={longitude}&appid={api_key}'
    response = requests.get(url)
    return response.json()

# Transform
def transform_response(response):
    df = pd.json_normalize(response['list'])
    df['dt'] = pd.to_datetime(df['dt'], unit='s')
    df['main.aqi'] = df['main.aqi'].astype(int)
    df = df[['dt', 'main.aqi']]
    return df

# Process
key, mapbox_key = get_api_key()
latitude = st.text_input('Enter latitude:', value='40.7128')
longitude = st.text_input('Enter longitude:', value='-74.0060')

response_current = extract_current(latitude, longitude, key)
response_forecast = extract_forecast(latitude, longitude, key)

df_current = transform_response(response_current)
df_forecast = transform_response(response_forecast)

# Visualize with Plotly and Mapbox
if not df_current.empty and not df_forecast.empty:
    st.header('Current Air Pollution Data')
    st.write(df_current)

    fig_current = px.scatter_mapbox(df_current, lat='latitude', lon='longitude', color='main.aqi', size='main.aqi',
                                    color_continuous_scale='viridis', size_max=15, zoom=10,
                                    mapbox_style="carto-positron",
                                    mapbox_accesstoken=mapbox_key)
    st.plotly_chart(fig_current, use_container_width=True)

    st.header('Air Pollution Forecast')
    st.write(df_forecast)

    fig_forecast = px.line(df_forecast, x='dt', y='main.aqi', color='main.aqi', labels={'main.aqi': 'AQI'},
                           title='Air Pollution Forecast')
    st.plotly_chart(fig_forecast, use_container_width=True)
else:
    st.error('No data available. Please check your inputs and API keys.')
