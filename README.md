# 🌦️ City Weather Data Handler 🌦️

This project consists of two Python scripts, `Data_handler2.py` and `fetchData01.py`, that work together to fetch, store, and visualize weather data for multiple cities using the OpenWeatherMap API. The weather data is stored in an SQLite database, processed using `pandas`, and visualized using `matplotlib`. The project also uses `tkinter` to provide a simple GUI for interacting with the data.

## 📑 Table of Contents

- [📋 Requirements](#-requirements)
- [💻 Installation](#-installation)
- [🚀 Usage](#-usage)
  - [🌍 Fetching Weather Data](#-fetching-weather-data)
  - [🖥️ Using the GUI](#-using-the-gui)
  - [📊 Visualization Features](#-visualization-features)
- [🔧 Customization](#-customization)


## 📋 Requirements

- Python 3.x
- The following Python packages:
  - `pandas`
  - `requests`
  - `schedule`
  - `sqlite3` (part of the Python standard library)
  - `tkinter` (part of the Python standard library)
  - `matplotlib`

To install the required packages, run:

```bash
pip install pandas requests schedule matplotlib
```

## 💻 Installation

1. Clone the repository or download the two Python scripts (`Data_handler2.py` and `fetchData01.py`).
2. Ensure that you have Python 3.x installed.
3. Install the required packages listed in the [Requirements](#-requirements) section.

## 🚀 Usage

### 🌍 Fetching Weather Data

1. Open the `fetchData01.py` file.
2. Replace the `API_KEY` variable with your own API key from the [OpenWeatherMap](https://openweathermap.org/api) website.
   
   ```python
   API_KEY = 'your_api_key_here'
   ```

3. Run `fetchData01.py` to fetch weather data for the cities listed in the `City_list` variable. The weather data will be saved in a SQLite database.

   ```bash
   python fetchData01.py
   ```

4. You will be prompted to enter the name for the SQLite database and the interval (in minutes) for fetching data.

   Example:
   ```
   Enter the FIle Name :  weather_data
   Enter the interval in minutes (default is 1): 5
   ```

   This will create a SQLite database named `weather_data.db` and fetch weather data every 5 minutes.

### 🖥️ Using the GUI

1. After fetching the weather data, run `Data_handler2.py`:

   ```bash
   python Data_handler2.py
   ```

2. The GUI will open, allowing you to visualize and compare weather data for different cities.

### 📊 Visualization Features

In the GUI, you can:

- **📍 Compare two cities**: Plot a comparison of a specific weather attribute (e.g., temperature, humidity) between two cities.
- **📈 Bar chart comparison**: Compare weather attributes (e.g., latest value, mean, max, min) across multiple cities.
- **🌡️ City-specific plots**: View the weather data for a single city, including min, max, and mean values.
- **📂 Export to CSV**: Export the weather data for a specific city to a CSV file.

## 🔧 Customization

### 🏙️ Adding or Removing Cities

To modify the list of cities for which you want to fetch weather data, edit the `City_list` variable in `fetchData01.py`:

```python
City_list = ["Hong Kong", "New York, US", "Tokyo, JP", "Sydney, AU", ...]
```



