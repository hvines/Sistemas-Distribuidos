#Tarea 1

#Descripción general

Este proyecto despliega, mediante Docker Compose, un flujo de procesamiento de eventos de tráfico extraídos de la API de Waze:
	-	Scraper: obtiene los últimos eventos de la zona de Santiago cada segundo y los almacena en MongoDB.
	-	MongoDB: base de datos NoSQL que actúa como fuente de verdad histórica.
	-	Cache (Redis): almacena el último lote de eventos durante 10 segundos para lecturas rápidas.
	-	Generador de tráfico: simula llegadas de eventos con dos distribuciones (determinista y Poisson) y postea a la API interna.
	-	UIs de administración: mongo-express en el puerto 8081 y redis-commander en el 8082.

3. Detalle de cada componente
	•	docker-compose.yml
Define todos los servicios y su orquestación:
	•	mongodb (mongo:6.0) con volumen mongo_data.
	•	mongo-express: interfaz web sin Basic Auth (ME_CONFIG_BASICAUTH=false).
	•	redis: almacén en memoria con healthcheck de PING.
	•	redis-commander: UI para Redis.
	•	waze-scraper (./scraper/app.py): script Python que:
	•	Lee MONGO_URI y REDIS_HOST.
	•	Inserta eventos en Mongo y cachea en Redis con TTL 10s (cache.setex("latest_alerts", 10, ...)).
	•	traffic-generator (./traffic-generator/generator.py): script Python que:
	•	Lee GENERATOR_API_URL, EVENTS_PER_SEC y DISTRIBUTION.
	•	Simula alertas con make_random_alert().
	•	Distribución determinista (interval = 1/rate) o Poisson (random.expovariate(rate)).
	•	scraper/app.py
	•	Conexión a MongoDB via MongoClient(mongo_uri).
	•	Índice único por uuid.
	•	Bucle de ejecución cada 1 segundo.
	•	traffic-generator/generator.py
	•	Interfaz HTTP de ingestión (POST JSON).
	•	Parámetros:
	•	EVENTS_PER_SEC: tasa media de eventos (por defecto 5 evt/s).
	•	DISTRIBUTION: deterministic o poisson.
	•	redis.conf (opcional)
	•	Parámetros como maxmemory-policy o persistencia pueden ajustarse aquí.

4. Instrucciones de arranque
	1.	Clonar o descargar el repositorio.
	2.	Configurar variables de entorno si deseas sobreescribir valores por defecto:
	•	MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD
	•	GENERATOR_API_URL, EVENTS_PER_SEC, DISTRIBUTION
	3.	Ejecutar:

docker-compose down --volumes  # limpia datos previos
docker-compose up -d          # construye y arranca todos los servicios


	4.	Verificar servicios corriendo:

docker-compose ps


	5.	Acceder a las UIs:
	•	Mongo Express → http://localhost:8081
	•	Redis Commander → http://localhost:8082

5. Explicación de parámetros

Parámetro	Servicio	Descripción	Valor por defecto
EVENTS_PER_SEC	traffic-generator	Tasa media de generación de eventos (evt/s).	5
DISTRIBUTION	traffic-generator	Distribución de llegadas: deterministic o poisson.	deterministic
MONGO_URI	waze-scraper	Cadena de conexión a MongoDB con autenticación.	mongodb://root:example@mongodb:27017/?authSource=admin
REDIS_HOST	waze-scraper	Host de Redis para cache.	redis
TTL latest_alerts (s)	waze-scraper (Redis)	Tiempo de vida de los datos cacheados en segundos.	10

Estos parámetros pueden ajustarse en el docker-compose.yml o mediante variables de entorno.
