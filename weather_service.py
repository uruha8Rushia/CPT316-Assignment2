import requests
from datetime import datetime
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


class OpenWeatherMapService(WeatherAPIBase):
    """
    OpenWeatherMap API implementation (Demonstrates Inheritance)
    """
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self._base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, city: str, units: str = "metric") -> Optional[Dict]:
        """
        Fetch current weather data for a city
        """
        params = {
            'q': city,
            'units': units
        }
        return self._make_request("/weather", params)
    
    def get_forecast(self, city: str, units: str = "metric") -> Optional[Dict]:
        """
        Fetch 5-day weather forecast
        """
        params = {
            'q': city,
            'units': units
        }
        return self._make_request("/forecast", params)
    
    def get_weather_by_coordinates(self, lat: float, lon: float, units: str = "metric") -> Optional[Dict]:
        """
        Fetch weather by geographic coordinates
        """
        params = {
            'lat': lat,
            'lon': lon,
            'units': units
        }
        return self._make_request("/weather", params)


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
    def process_current_weather(raw_data: Dict) -> Dict:
        """
        Process current weather data into structured format
        """
        if not raw_data:
            return {"error": "No data available"}
        
        weather_obj = WeatherData(raw_data)
        
        return {
            "location": {
                "city": weather_obj.get_city_name(),
                "country": weather_obj.get_country(),
                "coordinates": {
                    "lat": raw_data.get('coord', {}).get('lat', 0),
                    "lon": raw_data.get('coord', {}).get('lon', 0)
                }
            },
            "current": {
                "temperature": weather_obj.get_temperature(),
                "feels_like": weather_obj.get_feels_like(),
                "temp_min": raw_data.get('main', {}).get('temp_min', 0),
                "temp_max": raw_data.get('main', {}).get('temp_max', 0),
                "humidity": weather_obj.get_humidity(),
                "pressure": weather_obj.get_pressure(),
                "description": weather_obj.get_description(),
                "icon": weather_obj.get_icon()
            },
            "wind": {
                "speed": weather_obj.get_wind_speed(),
                "direction": weather_obj.get_wind_direction()
            },
            "timestamp": weather_obj.get_timestamp(),
            "sunrise": datetime.fromtimestamp(raw_data.get('sys', {}).get('sunrise', 0)).strftime('%H:%M:%S'),
            "sunset": datetime.fromtimestamp(raw_data.get('sys', {}).get('sunset', 0)).strftime('%H:%M:%S')
        }
    
    @staticmethod
    def process_forecast(raw_data: Dict) -> Dict:
        """
        Process forecast data into structured format
        """
        if not raw_data or 'list' not in raw_data:
            return {"error": "No forecast data available"}
        
        forecast_list = []
        daily_data = {}
        
        for item in raw_data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            date_str = dt.strftime('%Y-%m-%d')
            
            forecast_item = {
                "datetime": dt.strftime('%Y-%m-%d %H:%M:%S'),
                "date": date_str,
                "time": dt.strftime('%H:%M'),
                "temperature": item['main']['temp'],
                "feels_like": item['main']['feels_like'],
                "temp_min": item['main']['temp_min'],
                "temp_max": item['main']['temp_max'],
                "humidity": item['main']['humidity'],
                "pressure": item['main']['pressure'],
                "description": item['weather'][0]['description'],
                "icon": item['weather'][0]['icon'],
                "wind_speed": item['wind']['speed'],
                "clouds": item.get('clouds', {}).get('all', 0),
                "rain_3h": item.get('rain', {}).get('3h', 0)
            }
            
            forecast_list.append(forecast_item)
            
            # Group by day for daily summary
            if date_str not in daily_data:
                daily_data[date_str] = []
            daily_data[date_str].append(forecast_item)
        
        # Calculate daily summaries
        daily_summary = []
        for date, items in daily_data.items():
            temps = [i['temperature'] for i in items]
            daily_summary.append({
                "date": date,
                "temp_avg": round(sum(temps) / len(temps), 1),
                "temp_min": min(temps),
                "temp_max": max(temps),
                "description": items[len(items)//2]['description'],  # midday description
                "icon": items[len(items)//2]['icon']
            })
        
        return {
            "city": raw_data['city']['name'],
            "country": raw_data['city']['country'],
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
        self.weather_service = OpenWeatherMapService(api_key)
        self.data_processor = DataProcessor()
        self.cache = WeatherCache()
    
    def get_current_weather(self, city: str, use_cache: bool = True) -> Dict:
        """
        Get processed current weather data
        """
        cache_key = f"current_{city}"
        
        if use_cache:
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return cached_data
        
        raw_data = self.weather_service.get_current_weather(city)
        processed_data = self.data_processor.process_current_weather(raw_data)
        
        if use_cache and 'error' not in processed_data:
            self.cache.set(cache_key, processed_data)
        
        return processed_data
    
    def get_forecast(self, city: str, use_cache: bool = True) -> Dict:
        """
        Get processed forecast data
        """
        cache_key = f"forecast_{city}"
        
        if use_cache:
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return cached_data
        
        raw_data = self.weather_service.get_forecast(city)
        processed_data = self.data_processor.process_forecast(raw_data)
        
        if use_cache and 'error' not in processed_data:
            self.cache.set(cache_key, processed_data)
        
        return processed_data
    
    def get_complete_weather_info(self, city: str) -> Dict:
        """
        Get complete weather information (current + forecast + statistics)
        """
        current = self.get_current_weather(city)
        forecast = self.get_forecast(city)
        
        statistics = {}
        if 'forecast_3h' in forecast:
            statistics = self.data_processor.calculate_weather_statistics(
                forecast['forecast_3h']
            )
        
        return {
            "current_weather": current,
            "forecast": forecast,
            "statistics": statistics
        }


