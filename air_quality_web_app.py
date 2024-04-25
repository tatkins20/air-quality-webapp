import streamlit as st
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import folium

# Extract
def get_api_key():
    key = st.secrets['appid']
    return key

def get_air_data(city):
    getUrl = f'https://api.openaq.org/v1/latest?city={city}&limit=1'
    response = requests.get(getUrl)
    data = json.loads(response.text)
    return data[0] if len(data) > 0 else None

def main():
    st.title("Air Quality")
    city = st.text_input("Enter City Name:", "New York")
    search_button = st.button("Search")

    if search_button:
        result = get_air_data(city)
        if result is not None:
            st.write(f'City:
            {result["city"]}')
            st.write(f'Country:
            {result["country"]}')
            st.write(f'Current AQI:
            {result["aqi"]}')
            st.write(f'Last Updated:
            {result["last_updated"]}')

     m = folium.Map(location=[float(result["coord"]["lat"]), float(result["coord"]["lon"])], zoom_start=12)
            folium.Marker([float(result["coord"]["lat"]), float(result["coord"]["lon"])], popup="Air Quality Station").add_to(m)
            fig = plt.figure(figsize=(8,6))
            sns.lineplot(x='datetime', y='value', data=result['data'])
            plt.xticks(rotation=90)
            plt.xlabel('Time')
            plt.ylabel('AQI')
            st.pyplot(fig)
            st.write(m)
        else:
            st.write("No results found! Please try again.")

    st.set_page_config(layout="wide")

if __name__ == "__main__":
    main()
