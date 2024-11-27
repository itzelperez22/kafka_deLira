import matplotlib.pyplot as plt
from pymongo import MongoClient
from collections import Counter
import numpy as np

type_translation = {
    'normal': 'Normal',
    'fire': 'Fuego',
    'water': 'Agua',
    'electric': 'Eléctrico',
    'grass': 'Planta',
    'ice': 'Hielo',
    'fighting': 'Lucha',
    'poison': 'Veneno',
    'ground': 'Tierra',
    'flying': 'Volador',
    'psychic': 'Psíquico',
    'bug': 'Bicho',
    'rock': 'Roca',
    'ghost': 'Fantasma',
    'dragon': 'Dragón',
    'dark': 'Siniestro',
    'steel': 'Acero',
    'fairy': 'Hada'
}

client = MongoClient('localhost', 27017)
db = client.data_pipeline
pokemon_collection = db.pokemon_data
weather_collection = db.weather_data
marvel_collection = db.marvel_data

marvel_data = marvel_collection.find({}, {'name': 1, 'comics_count': 1, 'series_count': 1})

names = []
comics_counts = []
series_counts = []

for entry in marvel_data:
    names.append(entry['name'])
    comics_counts.append(entry['comics_count'])
    series_counts.append(entry['series_count'])

plt.figure(figsize=(10, 6))
plt.bar(names, comics_counts, color='blue', alpha=0.5, label='Comics Count')
plt.bar(names, series_counts, color='green', alpha=0.5, label='Series Count')
plt.xlabel('Personaje')
plt.ylabel('Cantidad')
plt.title('Cantidad de comics y series por personaje')
plt.xticks(rotation=90)
plt.legend()
plt.tight_layout()

pokemon_data = pokemon_collection.find({}, {'name': 1, 'types': 1})

type_counts = Counter()

for entry in pokemon_data:
    for ptype in entry['types']:
        translated_type = type_translation.get(ptype, ptype)  
        type_counts[translated_type] += 1

types = list(type_counts.keys())
counts = list(type_counts.values())

colors = plt.cm.tab20(np.linspace(0, 1, len(types)))

plt.figure(figsize=(12, 8))
plt.bar(types, counts, color=colors)
plt.xlabel('Tipo de Pokémon')
plt.ylabel('Cantidad de Pokémon')
plt.title('Cantidad de Pokémon por tipo (primeros 150)')
plt.xticks(rotation=90)
plt.tight_layout()

weather_data = weather_collection.find({}, {'state': 1, 'temperature': 1})

cities = []
temperatures = []

for entry in weather_data:
    cities.append(entry['state'])
    temperatures.append(entry['temperature'])

plt.figure(figsize=(12, 8))
plt.bar(cities, temperatures, color='orange', alpha=0.7)
plt.xlabel('Estado')
plt.ylabel('Temperatura (°C)')
plt.title('Temperatura por estado en México')
plt.xticks(rotation=90)
plt.tight_layout()

plt.show()
