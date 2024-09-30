import requests
import pandas as pd
import schedule
import time
import csv
from datetime import datetime
import sqlite3
from tkinter import *
from tkinter import messagebox, simpledialog, scrolledtext
import matplotlib.pyplot as plt
import os

connectDB = 'test930.db'

def fetch_weather_data(city):
    
    API_KEY = ''  #-------------> your api key from https://openweathermap.org/api
   
    API_URL = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    conn = sqlite3.connect(connectDB)
    cursor = conn.cursor()
    response = requests.get(API_URL.format(API_KEY))
    if response.status_code == 200:
        data = response.json()
        #print('succ')
        # weather_data = {
        #     'timestamp': datetime.now(),
        #     'temperature': data['main']['temp'],
        #     'humidity': data['main']['humidity'],
        #     'weather': data['weather'][0]['description'],
        # }
        

        sorce_mainDictHK = data['main'] | data['weather'][0] | data['wind'] 
        sorce_mainDictHK['visibility'] = data['visibility']
        sorce_mainDictHK['timestamp'] = datetime.now()

        #print(sorce_mainDictHK.keys())
        
        sanitized_city = ''.join(e for e in city if e.isalnum())

                            
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {sanitized_city}_weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temp REAL,
                feels_like REAL,
                temp_min REAL,
                temp_max REAL,
                pressure INTEGER,
                humidity INTEGER,
                sea_level INTEGER,
                grnd_level INTEGER,
                main TEXT,
                description TEXT,
                icon TEXT,
                speed REAL,
                deg INTEGER,
                visibility INTEGER,
                timestamp TEXT
            )
        ''')
        
        
        cursor.execute(f'''
                    INSERT INTO {sanitized_city}_weather (
                        temp, feels_like, temp_min, temp_max, pressure, humidity,
                        sea_level, grnd_level, main, description, icon,
                        speed, deg,  visibility, timestamp
                    ) VALUES (
                        :temp, :feels_like, :temp_min, :temp_max, :pressure, :humidity,
                        :sea_level, :grnd_level, :main, :description, :icon,
                        :speed, :deg,  :visibility, :timestamp
                    )
                    ''', sorce_mainDictHK)
        
        
        
        conn.commit()
        conn.close()
        print(f'ok {city}')
        

City_list = ["Hong Kong","New York, US","Tokyo, JP","Sydney, AU"
             ,"Los Angeles, US","Paris, FR","Berlin, DE","Moscow, RU"
             ,"Beijing, CN","Singapore, SG","Seoul, KR","Bangkok, TH","Toronto, CA",
             "Shanghai, CN","Abu Dhabi, AE","Chicago, US","Las Vegas, US",]


count = 1
def fetch_cityWether():
    global count
    for city in City_list:
        fetch_weather_data(city)
    print(count)
    count = count +  1
        

def main():
    
    interval = input("Enter the interval in minutes (default is 1): ")
    interval = int(interval) if interval.isdigit() else 1

    schedule.every(interval).minutes.do(fetch_cityWether)
    
    print(f"Scheduler started. Fetching weather data every {interval} minute(s).")
    
    while True:
        schedule.run_pending()
        time.sleep(1)
        
        



if __name__ == "__main__":
   
    file_name = input("Enter the FIle Name :  ")
    connectDB = f'{file_name}.db'
    fetch_cityWether()
    main()
    


