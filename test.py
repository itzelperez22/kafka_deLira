import requests
import json
import time
import hashlib
from pprint import pprint
from tabulate import tabulate

# Configuración de las APIs
marvel_public_key = '18a2a4bf108a15fe3cc0af6e9d25ee95'
marvel_private_key = '5a6d41de9d5ea3f003eddc87d9f6320803841a87'
ts = str(int(time.time()))
hash_string = f"{ts}{marvel_private_key}{marvel_public_key}"
hash_result = hashlib.md5(hash_string.encode()).hexdigest()
marvel_url = f"http://gateway.marvel.com/v1/public/characters?ts={ts}&apikey={marvel_public_key}&hash={hash_result}"

# Lista para almacenar los datos de los personajes
characters_data = []

# Realizar la solicitud a la API de Marvel
response = requests.get(marvel_url)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Convertir la respuesta a formato JSON
    data = response.json()
    
    # Iterar sobre cada personaje en los resultados de la respuesta
    for character in data["data"]["results"]:
        # Obtener el nombre y la descripción del personaje
        name = character["name"]
        
        # Obtener el número de cómics y series disponibles para el personaje
        comics_count = character["comics"]["available"]
        series_count = character["series"]["available"]
        
        # Agregar los datos del personaje a la lista
        characters_data.append({
            "name": name,
            "comics_count": comics_count,
            "series_count": series_count
        })

# Crear una tabla con los datos de los personajes
table = tabulate(characters_data, headers="keys", tablefmt="grid")


# Imprimir los datos de los personajes
print(table)
