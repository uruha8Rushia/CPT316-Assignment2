import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

class WeatherAPIBase:
    """
    Base class for weather API services (Demonstrates Inheritance)
    """
    def __init__(self, api_key: str):
        self._api_key = api_key  # Encapsulation: private attribute
        self._base_url = ""
    
    def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """
        Protected method for making API requests (Encapsulation)
        """
        try:
            params['appid'] = self._api_key
            response = requests.get(f"{self._base_url}{endpoint}", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return None


class OpenMeteoService:
    """
    Open-Meteo API implementation for all weather data (Free, No Key)
    """
    def __init__(self):
        self._base_url = "https://api.open-meteo.com/v1/forecast"
        self._geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    
    def get_coordinates(self, city: str) -> Optional[Dict]:
        """
        Geocode city name to coordinates
        """
        params = {
            'name': city,
            'count': 1,
            'language': 'en',
            'format': 'json'
        }
        try:
            response = requests.get(self._geocoding_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data and 'results' in data and len(data['results']) > 0:
                return data['results'][0]
            return None
        except requests.exceptions.RequestException as e:
            print(f"Geocoding Error: {e}")
            return None

    def get_weather_data(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Fetch comprehensive weather data (Current + Forecast)
        """
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,pressure_msl,wind_speed_10m,wind_direction_10m,weather_code',
            'hourly': 'temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,weather_code,precipitation_probability',
            'daily': 'temperature_2m_max,temperature_2m_min,temperature_2m_mean,weather_code,sunrise,sunset',
            'timezone': 'auto'
        }
        try:
            response = requests.get(self._base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"OpenMeteo API Error: {e}")
            return None

    def get_historical_weather(self, lat: float, lon: float, days: int = 7) -> Optional[Dict]:
        """
        Fetch historical weather data for the last N days
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        params = {
            'latitude': lat,
            'longitude': lon,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'hourly': 'temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m',
            'daily': 'temperature_2m_max,temperature_2m_min,temperature_2m_mean',
            'timezone': 'auto'
        }
        
        try:
            response = requests.get(self._base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"OpenMeteo API Error: {e}")
            return None





class WeatherData:
    """
    Weather data model class (Demonstrates Encapsulation)
    """
    def __init__(self, raw_data: Dict):
        self._raw_data = raw_data
        self._processed_data = {}
    
    def get_temperature(self) -> float:
        """Get temperature in specified units"""
        return self._raw_data.get('main', {}).get('temp', 0)
    
    def get_feels_like(self) -> float:
        """Get feels-like temperature"""
        return self._raw_data.get('main', {}).get('feels_like', 0)
    
    def get_humidity(self) -> int:
        """Get humidity percentage"""
        return self._raw_data.get('main', {}).get('humidity', 0)
    
    def get_pressure(self) -> int:
        """Get atmospheric pressure"""
        return self._raw_data.get('main', {}).get('pressure', 0)
    
    def get_wind_speed(self) -> float:
        """Get wind speed"""
        return self._raw_data.get('wind', {}).get('speed', 0)
    
    def get_wind_direction(self) -> int:
        """Get wind direction in degrees"""
        return self._raw_data.get('wind', {}).get('deg', 0)
    
    def get_description(self) -> str:
        """Get weather description"""
        weather = self._raw_data.get('weather', [{}])[0]
        return weather.get('description', 'N/A')
    
    def get_icon(self) -> str:
        """Get weather icon code"""
        weather = self._raw_data.get('weather', [{}])[0]
        return weather.get('icon', '')
    
    def get_city_name(self) -> str:
        """Get city name"""
        return self._raw_data.get('name', 'Unknown')
    
    def get_country(self) -> str:
        """Get country code"""
        return self._raw_data.get('sys', {}).get('country', '')
    
    def get_timestamp(self) -> str:
        """Get data timestamp"""
        dt = self._raw_data.get('dt', 0)
        return datetime.fromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S')


class DataProcessor:
    """
    Data processing class (Demonstrates Static Methods and Processing Logic)
    """
    @staticmethod
    def get_weather_description(code: int) -> str:
        """Map WMO weather code to description"""
        codes = {
            0: "Clear sky",
            1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
            95: "Thunderstorm"
        }
        return codes.get(code, "Unknown")

    @staticmethod
    def get_weather_icon(code: int) -> str:
        """Map WMO code to OpenWeatherMap icon equivalent (for compatibility)"""
        # Mapping logic could be more complex, but this is a basic mapping
        if code == 0: return "01d"
        if code in [1, 2]: return "02d"
        if code == 3: return "04d"
        if code in [45, 48]: return "50d"
        if code in [51, 53, 55, 61, 63, 65]: return "10d"
        if code in [71, 73, 75]: return "13d"
        if code >= 95: return "11d"
        return "03d"

    @staticmethod
    def process_current_weather(raw_data: Dict, city_info: Dict) -> Dict:
        """
        Process current weather data from Open-Meteo into structured format
        """
        if not raw_data or 'current' not in raw_data:
            return {"error": "No data available"}
        
        current = raw_data['current']
        daily = raw_data.get('daily', {})
        
        # Get today's daily data for sunrise/sunset
        sunrise = daily['sunrise'][0] if 'sunrise' in daily else None
        sunset = daily['sunset'][0] if 'sunset' in daily else None
        
        # Format timestamps
        sunrise_time = datetime.fromisoformat(sunrise).strftime('%H:%M:%S') if sunrise else "N/A"
        sunset_time = datetime.fromisoformat(sunset).strftime('%H:%M:%S') if sunset else "N/A"
        
        desc = DataProcessor.get_weather_description(current['weather_code'])
        icon = DataProcessor.get_weather_icon(current['weather_code'])
        
        return {
            "location": {
                "city": city_info.get('name', 'Unknown'),
                "country": city_info.get('country', ''),
                "coordinates": {
                    "lat": raw_data.get('latitude', 0),
                    "lon": raw_data.get('longitude', 0)
                }
            },
            "current": {
                "temperature": current['temperature_2m'],
                "feels_like": current['apparent_temperature'],
                "temp_min": daily['temperature_2m_min'][0] if 'temperature_2m_min' in daily else 0,
                "temp_max": daily['temperature_2m_max'][0] if 'temperature_2m_max' in daily else 0,
                "humidity": current['relative_humidity_2m'],
                "pressure": current['pressure_msl'],
                "description": desc,
                "icon": icon
            },
            "wind": {
                "speed": current['wind_speed_10m'],
                "direction": current['wind_direction_10m']
            },
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "sunrise": sunrise_time,
            "sunset": sunset_time
        }
    
    @staticmethod
    def process_forecast(raw_data: Dict, city_info: Dict) -> Dict:
        """
        Process forecast data into structured format
        """
        if not raw_data or 'hourly' not in raw_data:
            return {"error": "No forecast data available"}
        
        hourly = raw_data['hourly']
        times = hourly['time']
        
        forecast_list = []
        
        # Open-Meteo returns huge hourly arrays (7 days * 24h). We usually want next 5 days / 3h slots like OWM
        # Let's take every 3rd hour for the next 5 days
        
        current_time = datetime.now()
        
        for i in range(len(times)):
            dt = datetime.fromisoformat(times[i])
            
            # Skip past data
            if dt < current_time:
                continue
                
            # Stop after 5 days
            if (dt - current_time).days > 5:
                break
                
            date_str = dt.strftime('%Y-%m-%d')
            
            w_code = hourly['weather_code'][i]
            
            forecast_item = {
                "datetime": dt.strftime('%Y-%m-%d %H:%M:%S'),
                "date": date_str,
                "time": dt.strftime('%H:%M'),
                "temperature": hourly['temperature_2m'][i],
                "feels_like": hourly['temperature_2m'][i], # Approximate as apparent temp array might match
                "temp_min": hourly['temperature_2m'][i], # Hourly point
                "temp_max": hourly['temperature_2m'][i],
                "humidity": hourly['relative_humidity_2m'][i],
                "pressure": hourly['pressure_msl'][i],
                "description": DataProcessor.get_weather_description(w_code),
                "icon": DataProcessor.get_weather_icon(w_code),
                "wind_speed": hourly['wind_speed_10m'][i],
                "clouds": 0, # Not fetched in this query
                "rain_3h": 0
            }
            
            forecast_list.append(forecast_item)
        
        # Filter to 3-hourly to match OWM structure roughly (00, 03, 06...)
        forecast_list = [f for f in forecast_list if int(f['time'].split(':')[0]) % 3 == 0]

        # Calculate daily summaries
        daily = raw_data.get('daily', {})
        daily_summary = []
        
        if 'time' in daily:
            for i in range(len(daily['time'])):
                d_time = daily['time'][i]
                d_date = datetime.fromisoformat(d_time)
                
                # Skip past
                if d_date.date() < current_time.date():
                    continue
                    
                code = daily['weather_code'][i]
                
                daily_summary.append({
                    "date": d_time,
                    "temp_avg": daily['temperature_2m_mean'][i],
                    "temp_min": daily['temperature_2m_min'][i],
                    "temp_max": daily['temperature_2m_max'][i],
                    "description": DataProcessor.get_weather_description(code),
                    "icon": DataProcessor.get_weather_icon(code)
                })
        
        return {
            "city": city_info.get('name', 'Unknown'),
            "country": city_info.get('country', ''),
            "forecast_3h": forecast_list,
            "daily_summary": daily_summary
        }
    
    @staticmethod
    def calculate_weather_statistics(forecast_data: List[Dict]) -> Dict:
        """
        Calculate weather statistics from forecast data
        """
        if not forecast_data:
            return {}
        
        temperatures = [item['temperature'] for item in forecast_data]
        humidity_values = [item['humidity'] for item in forecast_data]
        
        return {
            "avg_temperature": round(sum(temperatures) / len(temperatures), 1),
            "max_temperature": max(temperatures),
            "min_temperature": min(temperatures),
            "avg_humidity": round(sum(humidity_values) / len(humidity_values), 1),
            "total_data_points": len(forecast_data)
        }
    
    @staticmethod
    def process_historical_weather(raw_data: Dict) -> Dict:
        """
        Process historical weather data
        """
        if not raw_data or 'hourly' not in raw_data:
            return {"error": "No historical data available"}
        
        hourly = raw_data['hourly']
        times = hourly['time']
        temps = hourly['temperature_2m']
        humidities = hourly['relative_humidity_2m']
        pressures = hourly['pressure_msl']
        winds = hourly['wind_speed_10m']
        
        history_points = []
        for i in range(len(times)):
            history_points.append({
                "timestamp": times[i], # ISO format in OpenMeteo
                "temperature": temps[i],
                "humidity": humidities[i],
                "pressure": pressures[i],
                "wind_speed": winds[i]
            })
            
        # Daily aggregation
        daily = raw_data.get('daily', {})
        daily_summary = []
        if 'time' in daily:
            for i in range(len(daily['time'])):
                daily_summary.append({
                    "date": daily['time'][i],
                    "max_temp": daily['temperature_2m_max'][i],
                    "min_temp": daily['temperature_2m_min'][i],
                    "avg_temp": daily['temperature_2m_mean'][i]
                })

        return {
            "hourly": history_points,
            "daily": daily_summary,
            "latitude": raw_data.get('latitude'),
            "longitude": raw_data.get('longitude')
        }


class WeatherCache:
    """
    Simple cache implementation to reduce API calls (Demonstrates Encapsulation)
    """
    def __init__(self, cache_duration: int = 600):
        self._cache = {}
        self._cache_duration = cache_duration  # seconds
    
    def get(self, key: str) -> Optional[Dict]:
        """Get cached data if not expired"""
        if key in self._cache:
            data, timestamp = self._cache[key]
            if (datetime.now().timestamp() - timestamp) < self._cache_duration:
                return data
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, data: Dict):
        """Store data in cache"""
        self._cache[key] = (data, datetime.now().timestamp())
    
    def clear(self):
        """Clear all cached data"""
        self._cache.clear()


class WeatherManager:
    """
    Main weather manager class coordinating all services (Demonstrates Composition)
    """
    def __init__(self, api_key: str):
        # API Key not needed for Open-Meteo but keeping arg for compatibility
        self.open_meteo_service = OpenMeteoService()
        self.data_processor = DataProcessor()
        self.cache = WeatherCache()
    
    def get_complete_weather_info(self, city: str) -> Dict:
        """
        Get complete weather information using Open-Meteo
        """
        # 1. Geocode
        city_info = self.open_meteo_service.get_coordinates(city)
        if not city_info:
            return {"error": f"City '{city}' not found"}
        
        lat = city_info['latitude']
        lon = city_info['longitude']
        
        # 2. Get Weather Data (Current + Forecast)
        raw_weather = self.open_meteo_service.get_weather_data(lat, lon)
        if not raw_weather:
            return {"error": "Failed to fetch weather data"}
            
        current = self.data_processor.process_current_weather(raw_weather, city_info)
        forecast = self.data_processor.process_forecast(raw_weather, city_info)
        
        # 3. Statistics
        statistics = {}
        if 'forecast_3h' in forecast:
            statistics = self.data_processor.calculate_weather_statistics(
                forecast['forecast_3h']
            )
        
        # 4. Historical Data
        raw_history = self.open_meteo_service.get_historical_weather(lat, lon)
        historical = self.data_processor.process_historical_weather(raw_history)
        
        return {
            "current_weather": current,
            "forecast": forecast,
            "statistics": statistics,
            "historical": historical
        }
    
    # Keeping these methods for compatibility if called individually
    def get_current_weather(self, city: str) -> Dict:
        city_info = self.open_meteo_service.get_coordinates(city)
        if not city_info: return {"error": "City not found"}
        raw = self.open_meteo_service.get_weather_data(city_info['latitude'], city_info['longitude'])
        return self.data_processor.process_current_weather(raw, city_info)

    def get_forecast(self, city: str) -> Dict:
        city_info = self.open_meteo_service.get_coordinates(city)
        if not city_info: return {"error": "City not found"}
        raw = self.open_meteo_service.get_weather_data(city_info['latitude'], city_info['longitude'])
        return self.data_processor.process_forecast(raw, city_info)


