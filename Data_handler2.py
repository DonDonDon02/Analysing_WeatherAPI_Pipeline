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
import tkinter as tk
from tkinter import ttk
import random
import os 
import fetchData01 as fetchData

root = Tk()
root.title("City Weather ")

root.geometry("1300x500")



file_ = []

for subdir, dirs, files in os.walk('./'):
    for file in files:
        if file.endswith('.db'):
            file_.append(file)




City_list = fetchData.City_list

col_list =[ 'temp', 'feels_like', 'temp_min', 'temp_max', 'pressure',
       'humidity', 'sea_level', 'grnd_level', 'main', 'description', 'icon',
       'speed', 'deg', 'visibility', 'timestamp']




#connectDB='Weather_Data_colab.db'
#connectDB ='WeatherData_03.db'

# def comfirm_connectDB()-> str:
    
    
#     return connectDB 


def get_df(country: str) -> pd.DataFrame :
    connectDB = selectFIleUI.get()
    
    sanitized_city = ''.join(e for e in country if e.isalnum())

    
    conn = sqlite3.connect(connectDB)
    cursor = conn.cursor()
    
    df = pd.read_sql_query(f'SELECT * FROM {sanitized_city}_weather', conn)
    conn.close()
    
    return df 


def get_ValueOfCity(country: str , value):
    connectDB = selectFIleUI.get()
    sanitized_city = ''.join(e for e in country if e.isalnum())
    conn = sqlite3.connect(connectDB)
    query = f"SELECT * FROM {sanitized_city}_weather"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df[value]


def get_City_value(valueType):
    df_temps = {}

    for city in City_list:
        df_temps[city] = get_ValueOfCity(city,valueType)

    return pd.DataFrame(df_temps)


######################################################## \/   DA   \/    ########################################################    

def plot1_comapare2():
    
    city_combobox1 = city_comboboxUI1.get()
    city_combobox2 = city_comboboxUI2.get()
    compareTo =compareUI1.get()
    
    city1 = ''.join(e for e in city_combobox1 if e.isalnum())
    city2 = ''.join(e for e in city_combobox2 if e.isalnum())
    
    city1DF = get_df(city1)
    city2DF = get_df(city2)
    
    plt.plot(city1DF[compareTo] , marker='o', linestyle='-', color='b', label= city1)

    plt.plot(city2DF[compareTo], marker='o', linestyle='-', color='r', label=city2)

    # Add labels and title
    plt.xlabel('')
    plt.ylabel(compareTo)
    
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()

def plot2_barh_wheather():
    #['lastes','mean','MAX','min'])
    ValueType =compareUI1.get()
    compareBy =compareUI2.get()
    
    if compareBy == 'lastes' :
        df = get_City_value(ValueType).iloc[-1]
    elif compareBy == 'mean':
        df = round(get_City_value(ValueType).mean(),2)
    elif compareBy == 'MAX':
        df = get_City_value(ValueType).max()
    elif compareBy == 'min':
        df = get_City_value(ValueType).min()
    
    
    df_sorted = df.sort_values()
    ax = df_sorted.plot(kind='barh')
    for index, value in enumerate(df_sorted):
        ax.text(value, index, f'{value} {ValueType}', va='center', ha='right' if value < ax.get_xlim()[1] * 0.1 else 'left', color='black')
        
    
    plt.show()
    
def plot3_channel():
    city1 = city_comboboxUI1.get()
    compareTo1 =compareUI1.get()
    
    df = get_df(city1)
    
    
    
    min_value = df[compareTo1].min()
    mean_value = df[compareTo1].mean()
    max_value = df[compareTo1].max()

    # Plot the entire series
   

    # Plot min, mean, max as horizontal lines
    plt.axhline(y=min_value, color='r', linestyle='--', label='Min')
    plt.axhline(y=mean_value, color='g', linestyle='--', label='Mean')
    plt.axhline(y=max_value, color='y', linestyle='--', label='Max')
    
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()

def plotSigleLine():
    city_combobox1 = city_comboboxUI1.get()
    compareTo =compareUI1.get()
    
    city1 = ''.join(e for e in city_combobox1 if e.isalnum())
    
    city1DF = get_df(city1)
    
    city1DF['timestamp'] = pd.to_datetime(city1DF['timestamp'])

    hours = city1DF['timestamp'].dt.strftime('%H:%M')
    
    random_color = (random.random(), random.random(), random.random())
    #plt.figure(figsize=(8,5))
    plt.plot(city1DF[compareTo] , marker='o', color=random_color, label= city1)
    
    plt.xticks(ticks=range(len(hours)), labels=hours, rotation=45)

    
    last_index = len(city1DF[compareTo]) - 1
    last_value = city1DF[compareTo].iloc[-1]
    val1 = city1DF[compareTo].iloc[-1].astype(str)
    plt.text(last_index + 5, last_value, (city1 +"_"+compareTo +"_"+val1), fontsize=10, color=random_color,verticalalignment='bottom', horizontalalignment='right')

    plt.xlabel('')
    plt.ylabel(compareTo)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()

def out1_showAllINfo():
    
    cityOut1 = city_comboboxUI1.get()
    df =get_df(cityOut1)

    temp = df.iloc[-1]
    output.insert(END, f'{temp}\n\n')

def test2():
    ValueType =compareUI1.get()
    df = get_City_value(ValueType).iloc[:-1]
    
    output.insert(END, f' {df}  \n\n')
    
    
    
    
def clear_output():
    output.delete(1.0,END)
    
def exportTOcsv():
    
    city = city_comboboxUI1.get()
    sanitized_city = ''.join(e for e in city if e.isalnum())
    
    
    get_df(city).to_csv(f'{sanitized_city}_data.csv', index=False)
    

#######################################################  /\   DA  /\    ########################################################    



City_1_label = ttk.Label(root, text="City_1")
City_1_label.grid(row=0, column=0, pady=5)

City_2_label = ttk.Label(root, text="City_2")
City_2_label.grid(row=0, column=1, pady=5)

Compare_label = ttk.Label(root, text="Compare")
Compare_label.grid(row=0, column=2, pady=5)

# Dropdowns for city selection
city_comboboxUI1 = ttk.Combobox(root, values=City_list)
city_comboboxUI1.grid(row=1, column=0, padx=10, pady=10)
city_comboboxUI1.set("Hong Kong")

city_comboboxUI2 = ttk.Combobox(root, values=City_list)
city_comboboxUI2.grid(row=1, column=1, padx=10, pady=10)
city_comboboxUI2.set("Hong Kong")

compareUI1 = ttk.Combobox(root, values=col_list)
compareUI1.grid(row=1, column=2, padx=10, pady=10)
compareUI1.set("temp")

compareUI2 = ttk.Combobox(root, values=['lastes','mean','MAX','min'])
compareUI2.grid(row=3, column=2, padx=10, pady=10)
compareUI2.set("lastes")

selectFIleUI = ttk.Combobox(root, values=file_)
selectFIleUI.grid(row=2, column=3, padx=10, pady=10)
selectFIleUI.set("chose_dataset.db")

# Buttons
BTN1 = tk.Button(root, text="Compare City1 and City2", command=plot1_comapare2)
BTN1.grid(row=2, column=0, pady=5, sticky='ew')

BTN2 = tk.Button(root, text="Compare by Value Type", command=plot2_barh_wheather)
BTN2.grid(row=3, column=0, pady=5, sticky='ew')

BTN3 = tk.Button(root, text="Mean Values and Min/Max Channel", command=plot3_channel)
BTN3.grid(row=4, column=0, pady=5, sticky='ew')

BTN4 = tk.Button(root, text="Show Weather Details By City1", command=out1_showAllINfo)
BTN4.grid(row=5, column=0, pady=5, sticky='ew')

BTN5 = tk.Button(root, text="Show Plot By City1", command=plotSigleLine)
BTN5.grid(row=6, column=0, pady=5, sticky='ew')

BTN5 = tk.Button(root, text="clean", command=clear_output)
BTN5.grid(row=7, column=0, pady=5, sticky='ew')


# BTN6 = tk.Button(root, text="te2st", command=test2)
# BTN6.grid(row=6, column=1, pady=5, sticky='ew')

# BTN6 = tk.Button(root, text="teaaaaasa2st", command=test2 )
# BTN6.grid(row=0, column=3, pady=0, sticky='ew')

BTN6 = tk.Button(root, text="City 1 data to csv", command=exportTOcsv )
BTN6.grid(row=1, column=3, pady=5, sticky='ew')

# BTN6 = tk.Button(root, text="te2st", command=test2, width=10)
# BTN6.grid(row=0, column=4, pady=5, sticky='ew')

# BTN6 = tk.Button(root, text="te2st", command=test2, width=10)
# BTN6.grid(row=1, column=4, pady=5, sticky='ew')

# BTN6 = tk.Button(root, text="Comfirm", command=comfirm_connectDB, width=10)
# BTN6.grid(row=2, column=4, pady=5, sticky='ew')

# BTN6 = tk.Button(root, text="te2stte2stte2stte2st", command=test2, width=50)
# BTN6.grid(row=0, column=5, pady=5, sticky='ew')
# Instructions
instruction_label1 = ttk.Label(root, text=": Select City 1 and City 2 to compare with Type of Value")
instruction_label1.grid(row=2, column=1, columnspan=2, sticky='w')

instruction_label2 = ttk.Label(root, text=": Select Compare")
instruction_label2.grid(row=3, column=1, columnspan=2, sticky='w')

instruction_label3 = ttk.Label(root, text="")
instruction_label3.grid(row=4, column=1, columnspan=2, sticky='w')
# Checkboxes

# Scrolled Text Output
output = scrolledtext.ScrolledText(root, width=45, height=20)
output.grid(row=7, column=3, pady=10, sticky='n')




if __name__ == "__main__":
    
    
    #df =get_df('Hong Kong')
     
    #ValueType =compareUI1.get()
    
    #df = get_City_value('temp').iloc[-5:]
    #print(df)
    
    
    
    root.mainloop()

    