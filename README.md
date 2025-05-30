# Tarea 1

# Descripción general

Este proyecto despliega, mediante Docker Compose, un flujo de procesamiento de eventos de tráfico extraídos de la API de Waze:
1.	Scraper: obtiene los últimos eventos de la zona de Santiago cada segundo y los almacena en MongoDB.
2.	MongoDB: base de datos NoSQL que actúa como fuente de verdad histórica.
3.	Cache (Redis): almacena el último lote de eventos durante 10 segundos para lecturas rápidas.
4.	Generador de tráfico: simula llegadas de eventos con dos distribuciones (determinista y Poisson) y postea a la API interna.
5.	UIs de administración: mongo-express en el puerto 8081 y redis-commander en el 8082.


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
 
4.	Acceder a las UIs:

   
	Mongo Express → http://localhost:8081 y Redis Commander → http://localhost:8082

# Explicación de parámetros de distribución
 
 ```powershell
    
EVENTS_PER_SEC	traffic-generator	Tasa media de generación de eventos por segundo (evt/s).	5
DISTRIBUTION	traffic-generator	Distribución de llegadas: deterministic o poisson.	deterministic

 ```
Existe un parametro de distribución tanto determinista como poisson.
Por defecto está en poisso, pero cambiarlo a determinista, es sólo cambiar la linea 30 del generator.py a "deterministic".
