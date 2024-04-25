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

def extract_current(key, latitude, longitude):
    getUrl = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={key}'
    response = requests.get(getUrl)
    return response.json()

def extract_forecast(key, latitude, longitude):
    getUrl = f'https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={latitude}&lon={longitude}&appid={key}'
    response = requests.get(getUrl)
    return response.json()

# Transform
def transform_response(response):
    data = response.get('list', [])  # Get 'list' key from response, default to empty list if not found
    if not data:
        st.error("No data available")
        return pd.DataFrame()  # Return empty DataFrame if no data
    
    try:
        df = pd.json_normalize(data)
    except KeyError:
        st.error("No coordinate information available")
        return pd.DataFrame()  # Return empty DataFrame if no coordinate information
    
    # Extract latitude and longitude from 'coord' column if available
    if 'coord' in df.columns:
        df[['lat', 'lon']] = pd.DataFrame(df['coord'].tolist(), index=df.index)
        df.drop(columns=['coord'], inplace=True)
    else:
        st.error("No coordinate information available")
        return pd.DataFrame()  # Return empty DataFrame if no coordinate information
    
    return df

# The App in action
def main():
    st.title("Air Quality Data Visualization")

    # Input latitude and longitude
    latitude = st.sidebar.number_input('Enter Latitude:')
    longitude = st.sidebar.number_input('Enter Longitude:')

    if latitude and longitude:  # Check if latitude and longitude are provided
        # Process
        key, mapboxkey = get_api_key()
        response_current = extract_current(key, latitude, longitude)
        response_forecast = extract_forecast(key, latitude, longitude)
        
        try:
            df_current = transform_response(response_current)
            df_forecast = transform_response(response_forecast)

            # Visualize with Plotly and Mapbox
            if not df_current.empty:
                st.subheader('Current Air Pollution Data')
                fig_current = px.scatter_mapbox(df_current, lat='lat', lon='lon', hover_name='dt', hover_data=['main.aqi'], 
                                                 color='main.aqi', color_continuous_scale=px.colors.cyclical.IceFire, size='main.aqi', size_max=15, zoom=10)
                fig_current.update_layout(mapbox_style='open-street-map', mapbox_accesstoken=mapboxkey)
                st.plotly_chart(fig_current)

            if not df_forecast.empty:
                st.subheader('Forecasted Air Pollution Data')
                fig_forecast = px.line(df_forecast, x='dt', y='main.aqi', title='Air Quality Index Forecast', labels={'main.aqi': 'Air Quality Index'})
                st.plotly_chart(fig_forecast)
            
        except KeyError as e:
            st.error("Error occurred: {}".format(e))
    else:
        st.write('Please enter latitude and longitude to view air pollution data.')

if __name__ == "__main__":
    main()
