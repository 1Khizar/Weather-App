import streamlit as st
import requests

API_KEY = "API_KEY"  # Replace this with your actual API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Function to get weather data
def get_weather(city):
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f" HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Network error: {e}")
    return None

# Set page config
st.set_page_config(page_title="Weather Info", page_icon="🌦️", layout="centered")

# Title with emoji
st.markdown("<h1 style='text-align: center;'>🌤️ Weather Info App</h1>", unsafe_allow_html=True)

# Input
st.markdown("### 🔍 Enter a city to check its current weather:")
city = st.text_input("City Name", placeholder="e.g. Haripur")

# Get weather button
if st.button("Get Weather"):
    if city:
        data = get_weather(city)
        if data:
            st.success(f"✅ Weather data for **{data['name']}**")

            # Display in two columns
            col1, col2 = st.columns(2)

            with col1:
                st.metric("🌡️ Temperature (°C)", f"{data['main']['temp']}°C")
                st.metric("💧 Humidity", f"{data['main']['humidity']}%")
            with col2:
                st.metric("🌬️ Wind Speed", f"{data['wind']['speed']} m/s")
                st.metric("☁️ Condition", data['weather'][0]['description'].title())

            # Optional: Show detailed raw data if user expands
            with st.expander("📦 Show raw data"):
                st.json(data)

            # Save to file
            with st.expander("💾 Save and Download"):
                weather_str = f"""
City: {data['name']}
Temperature: {data['main']['temp']}°C
Wind Speed: {data['wind']['speed']} m/s
Humidity: {data['main']['humidity']}%
Weather: {data['weather'][0]['description'].title()}
"""
                # Save to file
                with open("weather_data.txt", "w") as file:
                    file.write(weather_str)

                st.success("✅ Weather data saved to file.")
                with open("weather_data.txt", "rb") as file:
                    st.download_button("📥 Download Weather Data", file, file_name="weather_data.txt")
        else:
            st.warning("City not found. Try again.")
    else:
        st.warning(" Please enter a city name.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Made by Khizar Ishtiaq</p>", unsafe_allow_html=True)
