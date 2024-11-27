from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# Configuración del consumidor de Kafka
consumer = KafkaConsumer(
    'marvel_topic',
    'weather_topic',
    'pokemon_topic',
    group_id='my_consumer_group',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=False
)



# Configuración de MongoDB
client = MongoClient('localhost', 27017)
db = client.data_pipeline
marvel_collection = db.marvel_data
marvel_collection.create_index('name', unique=True)
weather_collection = db.weather_data
weather_collection.create_index('state', unique=True)
pokemon_collection = db.pokemon_data
pokemon_collection.create_index('name', unique=True)

# Consumir y almacenar mensajes en MongoDB
for message in consumer:
    topic = message.topic
    print(f"Recibido mensaje de {topic}")
    
    if topic == 'pokemon_topic':
        try:
            pokemon_data = {
                'name': message.value['name'],
                'types': [ptype['type']['name'] for ptype in message.value['types']]
            }
            pokemon_collection.insert_one(pokemon_data)
            consumer.commit()
        except KeyError as e:
            print("Error al procesar datos de Pokémon", e)
        except Exception as e:
            print("Documento duplicado, abortando inserción")
    
    elif topic == 'weather_topic':
        try:
            weather_data = {
                'state': message.value['name'],
                'temperature': message.value['main']['temp'],
                'timestamp': message.value['dt']                
            }
            weather_collection.insert_one(weather_data)
            consumer.commit()
        except KeyError as e:
            print("Error general", e)
        except Exception as e:
            print("Documento duplicado, abortando inserción")

    elif topic == 'marvel_topic':
        try:
            characters = []
            for character in message.value['data']['results']:
                character_data = {
                    'name': character['name'],
                    'comics_count': character['comics']['available'],
                    'series_count': character['series']['available']
                }   
                characters.append(character_data)
            marvel_collection.insert_many(characters)
            consumer.commit()
        except KeyError as e:
            print("Error general", e)
        except Exception as e:
            print("Documento duplicado, abortando inserción")


