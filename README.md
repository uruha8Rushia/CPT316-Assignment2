# Weather Dashboard API

A Flask-based REST API for retrieving weather data using the Open-Meteo API. This project includes Node-RED integration for workflow automation and data visualization.

## Features

- 🌡️ Get current weather data for any city
- 📅 Fetch 5-day weather forecasts
- 🔄 Node-RED flow integration
- 📊 Weather history tracking (CSV)
- ✅ Health check endpoints
- 🆓 Free Open-Meteo API (No API Key required)

## Prerequisites

- Python 3.8 or higher
- Node-RED (optional, for flow integration)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd assignment2
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Set up environment variables**
   
   No API key is required for Open-Meteo.

## Usage

1. **Start the Flask server**
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`

2. **API Endpoints**

   - `GET /` - API information
   - `GET /api/health` - Health check
   - `GET /api/weather/current?city=<city_name>` - Current weather
   - `GET /api/weather/forecast?city=<city_name>` - 5-day forecast
   - `GET /api/weather/complete?city=<city_name>` - Complete weather data

3. **Example requests**
   ```bash
   # Get current weather for London
   curl "http://localhost:5000/api/weather/current?city=London"
   
   # Get forecast
   curl "http://localhost:5000/api/weather/forecast?city=London"
   ```

## Node-RED Integration

Import the `node-red-flow.json` file into Node-RED to use the pre-configured weather dashboard workflow.

## Project Structure

```
.
├── app.py                  # Flask API server
├── weather_service.py      # Weather API service layer
├── requirements.txt        # Python dependencies
├── weather_history.csv     # Weather data history
├── node-red-flow.json      # Node-RED flow configuration
├── .env                    # Environment variables (not required)
└── README.md              # This file
```

## Technologies Used

- **Flask** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Requests** - HTTP library
- **Python-dotenv** - Environment variable management
- **Open-Meteo API** - Weather data provider

## Contributing

This is a university assignment project (CPT316). Feel free to fork and modify for your own learning purposes.

## License

This project is for educational purposes.

## Author

Created for CPT316 Assignment 2 - Universiti Sains Malaysia
