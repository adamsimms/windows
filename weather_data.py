import requests
from bs4 import BeautifulSoup
import time
import json

def get_weather_data():
    url = 'https://www.smartatlantic.ca/erddap/tabledap/DFO_Sutron_DOGIS.htmlTable'
    columns = ['station_name',
               'time',
               'wind_dir_avg',
               'wind_spd_gust_dir',
               'wind_spd_avg',
               'wind_spd_gust']
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    new_data_row = soup.findAll("table")[1].findAll('tr')[2]
    row_vals = new_data_row.findAll('td')[0].\
               text.split('\n')[:6]
    data_dict = {}
    for i, col in enumerate(columns):
        data_dict.update({col: float(row_vals[i]) if col not in ['station_name', 'time'] else row_vals[i]})
    return data_dict

def read_data():
    with open('data.txt', 'rt') as file:
        x = eval(file.read())
        return x

if __name__ == '__main__':
    while True:
        data_dict = get_weather_data()
        with open('data.txt', 'wt') as file:
            file.write(str(data_dict))
            file.close()
        print(data_dict)
        time.sleep(.1)
