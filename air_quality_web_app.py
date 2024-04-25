import streamlit as st
import requests
import json
import pandas as pd
import pytz
import os
import plotly.express as px

#Extract
def get_api_key():
    key = st.secrets['appid']
    mapboxkey = st.secrets['mapboxkey']
    return(key,mapboxkey)

def extract_current():
    getUrl='http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API key}'
    response = requests.request("GET", getUrl, params={"appid": key})
    return(json.loads(response.content.decode('utf-8')))

def extract_forecast():
    getUrl='http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={API key}'
    response = requests.request("GET", getUrl, params={"appid": key})
    return(json.loads(response.content.decode('utf-8')))

#Transform
def transform_response(response):
    data = response['list']
    df = pd.DataFrame(data)
    df['dt'] = pd.to_datetime(df['dt'], unit='s')
    df['dt'] = df['dt'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern') # Convert time to Eastern Time Zone
    df['main'] = df['main'].apply(pd.Series) # Expand 'main' column
    df = pd.concat([df.drop(['main'], axis=1), df['main'].apply(pd.Series)], axis=1) # Concatenate expanded 'main' column
    return df

# The App in action : Run custom functions if valid inputs are entered

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
    fig_current = px.scatter_mapbox(df_current, lat='coord.lat', lon='coord.lon', hover_name='dt', hover_data=['aqi', 'components'], color='aqi',
                                     color_continuous_scale=px.colors.cyclical.IceFire, size='aqi', size_max=15, zoom=10)
    fig_current.update_layout(mapbox_style='open-street-map', mapbox_accesstoken=mapboxkey)
    st.plotly_chart(fig_current)

    st.title('Forecasted Air Pollution Data')
    fig_forecast = px.line(df_forecast, x='dt', y='aqi', title='Air Quality Index Forecast', labels={'aqi': 'Air Quality Index'})
    st.plotly_chart(fig_forecast)
else:
    st.write('Please enter latitude and longitude to view air pollution data.')

#Visualize with Plotly and Mapbox
    # For the current air pollution data, use px.scatter_mapbox to visualize data in a map
    #For the forecast air pollution data, Use px.line to visualize data in a graph with with several lines
