from pymongo import MongoClient

# Configuración de MongoDB
client = MongoClient('localhost', 27017)
db = client.data_pipeline
marvel_collection = db.marvel_data

# Borrar toda la colección
marvel_collection.delete_many({})
