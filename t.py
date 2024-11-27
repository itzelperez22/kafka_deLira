import subprocess

# Nombre del tema que deseas verificar
topic = 'marvel_topic'

# Comando para obtener el número de mensajes en el tema dentro del contenedor de Kafka
command = f'docker-compose exec -T kafka1 kafka-run-class kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic {topic} --time -1'

# Ejecuta el comando
try:
    output = subprocess.check_output(command, shell=True, text=True)
    message_count = sum(int(line.split(':')[2]) for line in output.strip().split('\n'))
    print(f'El tema {topic} tiene {message_count} mensajes')
except subprocess.CalledProcessError as e:
    print(f'Error al obtener el número de mensajes del tema {topic}')
    print(e)
