# Hola, este es el repositorio del final de De Lira

Este repositorio consta de 3 archivos principales: `producer.py`, `consumer.py` y `docker-compose.yml`.

## PRODUCER

`producer.py` es el archivo que extrae información de las APIs, por el momento solo de la API de Marvel, y la envía a Kafka como un tópico.

## CONSUMER

`consumer.py` es el archivo que extrae información de los tópicos de Kafka y los inserta en la base de datos de MongoDB. En este caso específico para lo de Marvel, formatea los datos para conseguir el nombre del personaje y los números de cómics y series para este.

## COMPOSE

Luego tenemos `docker-compose.yml`. Este archivo se ejecuta en la línea de comandos como un comando de Docker. Deben estar en la carpeta donde se encuentra el archivo y usar:

    docker compose -f <nombre_del_archivo> up

Esto crea el contenedor con Kafka y Zookeeper. Deben dejar esa consola abierta para que funcionen. Si necesitan hacer otra cosa, abran otra consola.

Principalmente, eso es lo que vamos a usar. Tenemos que encender Kafka, ejecutar el `producer.py` y luego el `consumer.py`. El `producer.py` cada 60s (lo podemos cambiar) va a enviar tópicos a Kafka y el `consumer.py` cada vez que pueda va a insertar los tópicos en la base de datos. Por el momento no está configurada para que no se repitan documentos (hay que ponerlo).

Luego tenemos el `visualizer.py`, el cual lee los documentos de MongoDB y grafica en base a ellos. Aquí tengo una duda porque en el esquema de la tarea dice que el `consumer.py` envía a la base y grafica, así que no sé si esté bien graficar desde la base.

Los demás archivos son extras, ya sea para borrar la base de datos fácilmente, purgar los tópicos de Kafka o verificar cuántos tópicos hay en este.
