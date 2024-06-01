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

def get_coordinates(city, key):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={key}'
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        return None, None

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

# User input for city name
city = st.text_input("Enter City Name", value="")

if st.button("Get Data"):
    key, mapboxkey = get_api_key()
    lat, lon = get_coordinates(city, key)
    
    if lat is not None and lon is not None:
        response_current = extract_current(lat, lon, key)
        response_forecast = extract_forecast(lat, lon, key)
        
        if 'list' in response_current and 'list' in response_forecast:
            df_current = transform_response(response_current, lat, lon)
            df_forecast = transform_response(response_forecast, lat, lon)
            
            # Visualize with Plotly and Mapbox
            st.subheader("Current Air Pollution Data")
            fig_current = px.scatter_mapbox(
                df_current, lat='lat', lon='lon', size='main_aqi',
                color='main_aqi', 
                hover_data={
                    'components_co': 'CO', 
                    'components_no': 'NO', 
                    'components_no2': 'NO2', 
                    'components_o3': 'O3', 
                    'components_so2': 'SO2', 
                    'components_pm2_5': 'PM2.5', 
                    'components_pm10': 'PM10'
                },
                zoom=10, height=300,
                labels={'main_aqi': 'Air Quality Index', 'lat': 'Latitude', 'lon': 'Longitude'}
            )
            fig_current.update_layout(mapbox_style="open-street-map", mapbox_accesstoken=mapboxkey)
            st.plotly_chart(fig_current)
            
            st.subheader("Forecast Air Pollution Data")
            df_forecast['dt'] = pd.to_datetime(df_forecast['dt'], unit='s')
            fig_forecast = px.line(
                df_forecast, x='dt', y=[
                    'main_aqi', 'components_co', 'components_no', 'components_no2', 
                    'components_o3', 'components_so2', 'components_pm2_5', 'components_pm10'
                ],
                labels={
                    'value': 'Concentration', 
                    'variable': 'Pollutant', 
                    'dt': 'Date', 
                    'main_aqi': 'Air Quality Index', 
                    'components_co': 'CO', 
                    'components_no': 'NO', 
                    'components_no2': 'NO2', 
                    'components_o3': 'O3', 
                    'components_so2': 'SO2', 
                    'components_pm2_5': 'PM2.5', 
                    'components_pm10': 'PM10'
                }
            )
            st.plotly_chart(fig_forecast)
        else:
            st.error("Failed to retrieve data. Please check the inputs and try again.")
    else:
        st.error("Failed to retrieve coordinates. Please check the city name and try again.")
