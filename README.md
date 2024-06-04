## Air Pollution Data Viewer
This Streamlit app provides an intuitive interface to explore air pollution data for any city worldwide. It utilizes the OpenWeatherMap API to fetch current and forecasted air quality information, offering valuable insights into pollution levels and trends.

## Usage
You can immediately launch the app by visiting this link: Air Quality Web App. No local setup is required—simply open the link in your web browser and start using it!

## Features
City-based Air Pollution Data: Enter the name of any city in the text input field, and the app will retrieve its current air pollution data, including the Air Quality Index (AQI) and the concentration of various pollutants.
Interactive Visualizations: The app employs Plotly and Mapbox to create interactive charts. The "Current Air Pollution Data" section features a scatter mapbox chart, allowing you to visualize AQI values and explore detailed pollutant information by hovering over data points.
Forecasted Trends: The "Forecast Air Pollution Data" section displays a line chart that shows how AQI and individual pollutant concentrations are expected to change over time. You can select specific pollutants from the dropdown menu to focus on their forecasted trends.

## Example
![image](https://github.com/tatkins20/air-quality-webapp/assets/25071944/526d5f61-8a3c-418d-9087-6fdf3dbeaf8c)


## Setup (For Local Development)
If you wish to run the app locally and contribute to its development, follow these steps:

Clone the repository: git clone https://github.com/your-username/air-pollution-data-viewer.git\
Create a virtual environment: python -m venv env\
Activate the virtual environment:\
Windows: env\Scripts\activate\
MacOS/Linux: source env/bin/activate\
Install the required packages: pip install -r requirements.txt\
Obtain an API key from [OpenWeatherMap](https://openweathermap.org/api) and a [Mapbox access token](https://account.mapbox.com/access-tokens).\
Create a file named .streamlit/secrets.toml in the root directory of the project and add the following lines:\
appid = "your_openweathermap_api_key"\
mapboxkey = "your_mapbox_access_token"\
Replace your_openweathermap_api_key and your_mapbox_access_token with your actual credentials.\
Run the app: streamlit run app.py\
Open your web browser and navigate to the provided local URL (usually http://localhost:8501) to access the app.

## Credits
This app is built using Streamlit, a powerful framework for creating data-focused web applications. It leverages the OpenWeatherMap API for air pollution data retrieval and Mapbox for map visualization. Pandas is used for data manipulation, and Plotly for creating interactive charts.
