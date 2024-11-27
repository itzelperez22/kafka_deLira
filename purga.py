import subprocess

def delete_topic(topic):
    command = f'docker-compose exec -T kafka1 kafka-topics --delete --topic {topic} --bootstrap-server localhost:9092'
    try:
        subprocess.run(command, shell=True, check=True)
        print(f'Tema {topic} eliminado exitosamente.')
    except subprocess.CalledProcessError as e:
        print(f'Error al eliminar el tema {topic}.')
        print(e)

# Nombre del tema que deseas purgar
topic = 'marvel_topic'


# Eliminar el tema
delete_topic(topic)

topic = 'weather_topic'

delete_topic(topic)