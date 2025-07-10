import requests
from datetime import datetime
from tkinter import messagebox
import tkinter as tk

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city):
        """Get current weather for a city"""
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'  # For Celsius
            }
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                return {
                    'city': city,
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description'].title(),
                    'wind_speed': data['wind']['speed'],
                    'icon': data['weather'][0]['icon']
                }
            else:
                return None
        except Exception as e:
            print(f"Weather API error: {e}")
            return None
    
    def show_weather_window(self, parent, flight_info):
        """Show weather window with flight's source and destination weather"""
        if not flight_info:
            messagebox.showerror("Error", "No flight information provided")
            return
            
        source, destination, date = flight_info
        
        # Create weather window
        weather_window = tk.Toplevel(parent)
        weather_window.title("Flight Weather Information")
        weather_window.geometry("500x400")
        
        # Header
        tk.Label(weather_window, 
                text=f"Weather Forecast for Flight",
                font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(weather_window, 
                text=f"{source} to {destination} on {date}",
                font=("Arial", 12)).pack(pady=5)
        
        # Weather frames
        weather_frame = tk.Frame(weather_window)
        weather_frame.pack(pady=20)
        
        # Source weather
        source_frame = tk.Frame(weather_frame)
        source_frame.pack(side="left", padx=20)
        
        source_weather = self.get_weather(source)
        if source_weather:
            self._display_weather(source_frame, source_weather, "Departure")
        else:
            tk.Label(source_frame, text=f"Weather data not available\nfor {source}").pack()
        
        # Destination weather
        dest_frame = tk.Frame(weather_frame)
        dest_frame.pack(side="right", padx=20)
        
        dest_weather = self.get_weather(destination)
        if dest_weather:
            self._display_weather(dest_frame, dest_weather, "Arrival")
        else:
            tk.Label(dest_frame, text=f"Weather data not available\nfor {destination}").pack()
    
    def _display_weather(self, frame, weather_data, title):
        """Helper method to display weather information in a frame"""
        # Weather icon (using emoji as placeholder - you could use actual images)
        icon_map = {
            '01': '☀️',  # clear sky
            '02': '⛅',  # few clouds
            '03': '☁️',  # scattered clouds
            '04': '☁️',  # broken clouds
            '09': '🌧️',  # shower rain
            '10': '🌦️',  # rain
            '11': '⛈️',  # thunderstorm
            '13': '❄️',  # snow
            '50': '🌫️'   # mist
        }
        icon_code = weather_data['icon'][:2]
        weather_icon = icon_map.get(icon_code, '🌈')
        
        tk.Label(frame, 
                text=f"{title}: {weather_data['city']}\n{weather_icon}",
                font=("Arial", 14)).pack(pady=5)
        
        tk.Label(frame, 
                text=f"Temp: {weather_data['temperature']}°C\n"
                     f"Humidity: {weather_data['humidity']}%\n"
                     f"Conditions: {weather_data['description']}\n"
                     f"Wind: {weather_data['wind_speed']} m/s",
                font=("Arial", 12)).pack()