import requests
import json
from kafka import KafkaProducer
import time
import hashlib
import os 
from dotenv import load_dotenv
# Configuración de las APIs
marvel_public_key = "2383d7fdb54ce586d5c0c952a0132aba"
marvel_private_key = "678fafd6ecb865311774d25b4ea634f331cc2587"
openweather_key= "8e39ec354e7f204984d78a90f2696716"
ts = str(time.time())
hash_string = f"{ts}{marvel_private_key}{marvel_public_key}"
hash_result = hashlib.md5(hash_string.encode()).hexdigest()

# Índice de la página actual para la API de Marvel
marvel_page = 0

# Configuración del productor de Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Función para obtener datos de Marvel
def get_marvel_data(page):
    # Ajustar la URL para incluir el índice de la página actual
    marvel_url = f"http://gateway.marvel.com/v1/public/characters?ts={ts}&apikey={marvel_public_key}&hash={hash_result}&offset={page*20}"
    response = requests.get(marvel_url)
    return response.json()

def get_pokemon_data(pokemon_id):
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(pokemon_url)
    return response.json()

# Función para obtener datos de OpenWeather
def get_openweather_data(city_name):
    # Ajustar la URL para incluir la ciudad de interés
    openweather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={openweather_key}&units=metric"
    response = requests.get(openweather_url)
    return response.json()

# Publicar mensajes en Kafka

while marvel_page < 3:
    # Obtener datos de Marvel para la página actual
    marvel_data = get_marvel_data(marvel_page)
    
    # Enviar datos de Marvel a Kafka
    producer.send('marvel_topic', value=marvel_data)
    
    # Incrementar el índice de la página para la próxima llamada
    print("Marvel page: ", marvel_page)
    marvel_page += 1
    

    time.sleep(1)  # Esperar un minuto antes de la próxima llamada

for pokemon_id in range(1, 151):
    pokemon_data = get_pokemon_data(pokemon_id)
    producer.send('pokemon_topic', value=pokemon_data)
    print(f"Pokémon data sent to Kafka for Pokémon ID: {pokemon_id}")
print("Mensajes de Pokémon enviados a Kafka")
   
#lista con todas las ciudades de mexico para obtener el clima de openweathermap
mexico_cities = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", "Ciudad de Mexico","Coahuila", "Colima", "Durango", "Estado de México", "Estado de Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Estado de Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Estado de Zacatecas"]
for city in mexico_cities:
        weather_data = get_openweather_data(city)
        # Enviar datos de OpenWeather a Kafska
        producer.send('weather_topic', value=weather_data)
        print(weather_data)
        print(f"Weather data sent to Kafka for city: {city}")
print("Mensajes de clima enviados a Kafka")        
