import requests
from typing import Dict, Any
from langchain_core.tools import tool

def get_lat_lon(city_name: str) -> Dict[str, Any]:
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        response = requests.get(url)
        data = response.json()
        if not data.get("results"):
            return None
        result = data["results"][0]
        return {"latitude": result["latitude"], "longitude": result["longitude"], "name": result["name"]}
    except Exception as e:
        print(f"Error fetching location: {e}")
        return None

@tool
def get_current_weather(city: str) -> Dict[str, Any]:
    """Get the current weather for a specific city."""
    location = get_lat_lon(city)
    if not location:
        return {"error": f"Could not find location: {city}"}
    
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={location['latitude']}&longitude={location['longitude']}&current_weather=true"
        response = requests.get(url)
        data = response.json()
        current = data.get("current_weather", {})
        return {
            "location": location["name"],
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
            "weathercode": current.get("weathercode"),
            "time": current.get("time")
        }
    except Exception as e:
        return {"error": str(e)}

@tool
def get_forecast(city: str) -> Dict[str, Any]:
    """Get the weather forecast for a specific city."""
    location = get_lat_lon(city)
    if not location:
        return {"error": f"Could not find location: {city}"}
        
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={location['latitude']}&longitude={location['longitude']}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto"
        response = requests.get(url)
        data = response.json()
        daily = data.get("daily", {})
        return {
            "location": location["name"],
            "daily_forecast": [
                {
                    "date": date,
                    "max_temp": max_t,
                    "min_temp": min_t,
                    "code": code
                }
                for date, max_t, min_t, code in zip(
                    daily.get("time", []),
                    daily.get("temperature_2m_max", []),
                    daily.get("temperature_2m_min", []),
                    daily.get("weathercode", [])
                )
            ]
        }
    except Exception as e:
        return {"error": str(e)}
