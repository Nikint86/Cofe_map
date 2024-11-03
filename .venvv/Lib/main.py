import json
import os

import requests


from geopy import distance


from dotenv import load_dotenv


import folium


from flask import Flask


def fetch_coordinates(apikey, address):
    base_url = 'https://geocode-maps.yandex.ru/1.x'
    response = requests.get(base_url, params={
        'geocode': address,
        'apikey': apikey,
        'format': 'json',
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_func_distanse(cofies):
    return  cofies['Distanse']


def hello_world():
    with open('map.html') as file:
      return file.read()


my_file = open('coffee.json', 'r', encoding='CP1251')
file_contents = my_file.read()
cordinates = json.loads(file_contents)
my_file.close()
all_cofeina = cordinates
load_dotenv()
apikey = os.getenv('apikey')
inputcord = input()
coords = fetch_coordinates(apikey, inputcord)

cofe_spisok = list()

for all_cofeina in cordinates:
    all_cofeina_name =  all_cofeina['Name']
    all_cofeina_longitude = all_cofeina['Longitude_WGS84']
    all_cofeina_latitude = all_cofeina['Latitude_WGS84']
    all_cofeina_coordinates = [all_cofeina_longitude,all_cofeina_latitude]
    all_cofeina_coordinates_two = [all_cofeina_latitude,all_cofeina_longitude]
    func_distanse = (distance.distance(coords, all_cofeina_coordinates).km)
    cofee = dict()
    cofee['Name'] = all_cofeina_name
    cofee['Coordinates'] = all_cofeina_coordinates_two
    cofee['Distanse'] = func_distanse
    cofe_spisok.append(cofee)

min_distanse = sorted(cofe_spisok, key = get_func_distanse)
first_page = min_distanse[:5]
m = folium.Map(location=(coords[1],coords[0]),zoom_start=17)
first_cofe_marker = list()
first_cofe_name = list()
first_cofe_marker = first_page[1]
first_cofe_name = first_page[1]

for first_cofe_marker in first_page:
    folium.Marker(
    location= first_cofe_marker['Coordinates'],
    tooltip='Нажми на меня!',
    popup=first_cofe_name['Name'],
    icon=folium.Icon(color='green',icon='info-sign'),
    ).add_to(m)

folium.Marker(
    location= (coords[1],coords[0]),
    tooltip='Вы тут',
    popup='Вы тут',
    icon=folium.Icon(icon='star'),
    ).add_to(m)
m.save('map.html')


app = Flask(__name__)
app.add_url_rule('/', 'hello', hello_world)
app.run('0.0.0.0')
if __name__ == '__main__':
    main()