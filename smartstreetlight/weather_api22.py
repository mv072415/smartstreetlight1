import requests

API_KEY = "dcbbe2e5127feeec995acedb90f6354a"  # Replace with your actual API key
CITY = "Chennai"  # Change to your city
URL = f"http://api.openweathermap.org/data/2.5/weather?q={"Chennai"}&appid={"dcbbe2e5127feeec995acedb90f6354a"}&units=metric"

def get_weather():
    """Fetches weather data from OpenWeatherMap API."""
    try:
        response = requests.get(URL)
        data = response.json()

        if response.status_code == 200:
            weather = data["weather"][0]["main"]  # e.g., 'Clear', 'Rain', 'Clouds'
            temperature = data["main"]["temp"]  # Temperature in Celsius
            return weather, temperature
        else:
            print("Error fetching weather data:", data)
            return None, None

    except Exception as e:
        print("API request failed:", e)
        return None, None

# Test the function
if __name__ == "__main__":
    weather, temp = get_weather()
    print(f"Weather: {weather}, Temperature: {temp}°C")
