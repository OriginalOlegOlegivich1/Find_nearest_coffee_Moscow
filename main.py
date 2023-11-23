from flask import Flask
import folium
from geopy import distance
import requests
from pprint import pprint
import json
from dotenv import load_dotenv
import os
load_dotenv()







#функция для нахождения кордоу
def fetch_coordinates(yandex_geocoder_apikey, address):
    base_url = 'https://geocode-maps.yandex.ru/1.x'
    response = requests.get(base_url, params={  
        'geocode': address,
        'apikey': yandex_geocoder_apikey,
        'format': 'json',
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(' ')
    return lat,lon


#чобы дальше с жысоном работать 
with open('coffee.json', 'r', encoding='CP1251') as my_file:
  file_contents = my_file.read()
coffee_file_contents = json.loads(file_contents)


yandex_geocoder_apikey = os.getenv("APIKEY")  


user_place=input('Введите ваше место: ')
user_coords = fetch_coordinates(yandex_geocoder_apikey, user_place)

#список
coffee_shopes_with_distance=[] 
#словарь чобы найти данные о кафе
for cafe in coffee_file_contents:
  cafe_with_distance={
    'title':cafe['Name'],
    'latitude':cafe['geoData']['coordinates'][1],
    'longitude':cafe['geoData']['coordinates'][0],
    'distance':distance.distance(user_coords,(cafe['geoData']['coordinates'][1],cafe['geoData']['coordinates'][0])).km  
  }


  coffee_shopes_with_distance.append(cafe_with_distance)


def get_cafe_distance(cafe):
    return cafe['distance']
sorted_cafes=sorted(coffee_shopes_with_distance, key=get_cafe_distance)
five_nearest_cafes = sorted_cafes[0:5]


tooltip = 'Click me!'
m = folium.Map(location=user_coords)

folium.Marker(  
 [user_coords[0],user_coords[1]],
 popup=('Ваши собственные так называемые учёными из брухленского университета координаты'),
 tooltip=tooltip,
icon=folium.Icon(icon='red')).add_to(m)



for cafe in five_nearest_cafes:
  folium.Marker(
    [cafe['latitude'],cafe['longitude'] ], popup=cafe['title'], tooltip=tooltip
    ).add_to(m) 

m.save('index.html')

#сайт
def get_file_content(): 
   with open('index.html',encoding='UTF-8') as file:
      return file.read()
#сайт 2
app = Flask(__name__)
app.add_url_rule('/', 'это вирус хохохо ты зашёл на вирус хихихи',get_file_content )
app.run('0.0.0.0')















#coords = fetch_coordinates(apikey, 'Внуково')
#x=input('Введите ваше место: ')
#coords = fetch_coordinates(apikey, x)
#print(coords)

#a=input('Пункт А: ')
#n=input('Пункт Б: ')

#coords_a = fetch_coordinates(apikey, a)
#coords_n = fetch_coordinates(apikey, n)
#print(distance.distance(coords_a, coords_n).km)













