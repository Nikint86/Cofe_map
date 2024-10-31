import json


from itertools import product


import requests


import geopy


from geopy import distance


from pprint import pprint


import folium


from flask import Flask

if __name__ == '__main__':

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


my_file = open('coffee.json', 'r', encoding='CP1251')
file_contents = my_file.read()
cordinates = json.loads(file_contents)
my_file.close()
all_cofeina = cordinates
apikey = '17d42f3a-40e2-46e6-a82f-314e0bbbe9ed'
print('Где Вы находитесь?\n')
inputcord = input()
coords = fetch_coordinates(apikey, inputcord)
print('Ваши координаты:',coords)

cofe_spisok = list()

for all_cofeina in cordinates:
    all_cofeina_name =  all_cofeina['Name']
    all_cofeina_longitude = all_cofeina['Longitude_WGS84']
    all_cofeina_latitude = all_cofeina['Latitude_WGS84']
    all_cofeina_coordinates = [all_cofeina_longitude,all_cofeina_latitude]
    func_distanse = (distance.distance(coords, all_cofeina_coordinates).km)
    cofee = dict()
    cofee['Name'] = all_cofeina_name
    cofee['Coordinates'] = all_cofeina_coordinates
    cofee['Distanse'] = func_distanse
    cofe_spisok.append(cofee)

def get_func_distanse(cofies):
    return  cofies['Distanse']

min_distanse = sorted(cofe_spisok, key = get_func_distanse)
first_page = min_distanse[:5]
first_cofe_marker = (first_page[0]['Coordinates'])
first_cofe_name = (first_page[0]['Name'])
two_cofe_marker = (first_page[1]['Coordinates'])
two_cofe_name = (first_page[1]['Name'])
three_cofe_marker = (first_page[2]['Coordinates'])
three_cofe_name = (first_page[2]['Name'])
four_cofe_marker = (first_page[3]['Coordinates'])
four_cofe_name = (first_page[3]['Name'])
five_cofe_marker = (first_page[4]['Coordinates'])
five_cofe_name = (first_page[4]['Name'])

m = folium.Map(location=(coords[1],coords[0]),zoom_start=17)

folium.Marker(
    location=[first_cofe_marker[1],first_cofe_marker[0]],
    tooltip='Нажми на меня!',
    popup=first_cofe_name,
    icon=folium.Icon(icon='cloud'),
).add_to(m)

folium.Marker(
    location=[two_cofe_marker[1],two_cofe_marker[0]],
    tooltip='Нажми на меня!',
    popup=two_cofe_name,
    icon=folium.Icon(icon='cloud'),
).add_to(m)

folium.Marker(
    location=[three_cofe_marker[1],three_cofe_marker[0]],
    tooltip='Нажми на меня!',
    popup=three_cofe_name,
    icon=folium.Icon(icon='cloud'),
).add_to(m)

folium.Marker(
    location=[four_cofe_marker[1],four_cofe_marker[0]],
    tooltip='Нажми на меня!',
    popup=four_cofe_name,
    icon=folium.Icon(icon='cloud'),
).add_to(m)

folium.Marker(
    location=[five_cofe_marker[1],five_cofe_marker[0]],
    tooltip='Нажми на меня!',
    popup=five_cofe_name,
    icon=folium.Icon(icon='cloud'),
).add_to(m)

m.save('map.html')

def hello_world():
    with open('map.html') as file:
      return file.read()

app = Flask(__name__)
app.add_url_rule('/', 'hello', hello_world)
app.run('0.0.0.0')
