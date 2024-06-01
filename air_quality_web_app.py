import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px

# Extract
def get_api_key():
    key = st.secrets['appid']
    mapboxkey = st.secrets['mapboxkey']
    return key, mapboxkey

def extract_current(lat, lon, key):
    url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}'
    response = requests.get(url, params={"appid": key})
    return response.json()

def extract_forecast(lat, lon, key):
    url = f'https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}'
    response = requests.get(url, params={"appid": key})
    return response.json()

# Transform
def transform_response(response, lat, lon):
    data = response['list']
    df = pd.json_normalize(data, sep='_')
    df['lat'] = lat
    df['lon'] = lon
    return df

# The App in action: Run custom functions if valid inputs are entered
st.title("Air Pollution Data Viewer")

# User input for location
lat = st.number_input("Enter Latitude", value=0.0)
lon = st.number_input("Enter Longitude", value=0.0)

if st.button("Get Data"):
    key, mapboxkey = get_api_key()
    response_current = extract_current(lat, lon, key)
    response_forecast = extract_forecast(lat, lon, key)
    
    if 'list' in response_current and 'list' in response_forecast:
        df_current = transform_response(response_current, lat, lon)
        df_forecast = transform_response(response_forecast, lat, lon)
        
        # Visualize with Plotly and Mapbox
        st.subheader("Current Air Pollution Data")
        fig_current = px.scatter_mapbox(
            df_current, lat='lat', lon='lon', size='main_aqi',
            color='main_aqi', hover_data=['components_co', 'components_no', 'components_no2', 'components_o3', 'components_so2', 'components_pm2_5', 'components_pm10'],
            zoom=10, height=300)
        fig_current.update_layout(mapbox_style="open-street-map", mapbox_accesstoken=mapboxkey)
        st.plotly_chart(fig_current)
        
        st.subheader("Forecast Air Pollution Data")
        df_forecast['dt'] = pd.to_datetime(df_forecast['dt'], unit='s')
        fig_forecast = px.line(
            df_forecast, x='dt', y=['main_aqi', 'components_co', 'components_no', 'components_no2', 'components_o3', 'components_so2', 'components_pm2_5', 'components_pm10'],
            labels={'value': 'Concentration', 'variable': 'Pollutant'})
        st.plotly_chart(fig_forecast)
    else:
        st.error("Failed to retrieve data. Please check the inputs and try again.")
