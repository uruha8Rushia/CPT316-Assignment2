
# ============================================================================
# Flask API Server for Weather Dashboard
# ============================================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from weather_service import WeatherManager
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for Node-RED communication

# Initialize Weather Manager
weather_manager = WeatherManager()


@app.route('/')
def home():
	"""API information endpoint"""
	return jsonify({
		"service": "Weather Dashboard API",
		"version": "1.0",
		"endpoints": {
			"current": "/api/weather/current?city=<city_name>",
			"forecast": "/api/weather/forecast?city=<city_name>",
			"complete": "/api/weather/complete?city=<city_name>",
			"health": "/api/health"
		}
	})


@app.route('/api/health')
def health_check():
	"""Health check endpoint"""
	return jsonify({
		"status": "healthy",
		"timestamp": datetime.now().isoformat()
	})


@app.route('/api/weather/current')
def get_current_weather():
	"""Get current weather for a city"""
	city = request.args.get('city', 'London')
	use_cache = request.args.get('cache', 'true').lower() == 'true'
    
	try:
		data = weather_manager.get_current_weather(city, use_cache)
		return jsonify(data)
	except Exception as e:
		return jsonify({"error": str(e)}), 500


@app.route('/api/weather/forecast')
def get_forecast():
	"""Get weather forecast for a city"""
	city = request.args.get('city', 'London')
	use_cache = request.args.get('cache', 'true').lower() == 'true'
    
	try:
		data = weather_manager.get_forecast(city, use_cache)
		return jsonify(data)
	except Exception as e:
		return jsonify({"error": str(e)}), 500


@app.route('/api/weather/complete')
def get_complete_weather():
	"""Get complete weather information"""
	city = request.args.get('city', 'London')
    
	try:
		data = weather_manager.get_complete_weather_info(city)
		return jsonify(data)
	except Exception as e:
		return jsonify({"error": str(e)}), 500


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
	"""Clear the weather cache"""
	weather_manager.cache.clear()
	return jsonify({"message": "Cache cleared successfully"})


if __name__ == '__main__':
	print("=" * 60)
	print("Weather Dashboard API Server")
	print("=" * 60)
	print(f"Server starting on http://localhost:5000")
	print("=" * 60)
	app.run(debug=True, host='0.0.0.0', port=5000)
