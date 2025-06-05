# Tarea 2

# Descripción general

Este proyecto despliega, mediante Docker Compose, un flujo de procesamiento de eventos de tráfico extraídos de la API de Waze:
1.	Scraper: obtiene los últimos eventos de la zona de Santiago cada segundo y los almacena en MongoDB.
2.	MongoDB: base de datos NoSQL que almacena dichos eventos para luego pasar a su sistema de caché.
3.	Caché (Redis): almacena el último lote de eventos durante 10 segundos para consultas rápidas.
4.	Generador de tráfico: simula llegadas de eventos con dos distribuciones (determinista y Poisson).
5.	Visores para administración: mongo-express en el puerto 8081 y redis-commander en el 8082.





Cabe mencionar que el presente fue diseñado en un sistema con macOS 14.4.3.


# Instrucciones de arranque
1.	Clonar o descargar el repositorio.	
2.	Ejecutar:

    ```powershell
    
	docker-compose down --volumes  # limpia datos previos
	docker-compose up -d          # construye y arranca todos los servicios

    ```


3.	Verificar servicios corriendo:

    ```powershell

	docker-compose ps
	
 	```
 
4.	Acceder a los visores:

   
	Mongo Express → http://localhost:8081 y Redis Commander → http://localhost:8082

# Explicación de parámetros de distribución
 
 ```powershell
    
EVENTS_PER_SEC	traffic-generator	Tasa media de generación de eventos por segundo (evt/s).
DISTRIBUTION	traffic-generator	Distribución de llegadas: deterministic o poisson.	

 ```
Existe un parametro para una distribución tanto determinista como poisson.
Por defecto está en poisson, pero cambiarlo a determinista, es sólo cambiar la linea 30 del generator.py a "deterministic".

