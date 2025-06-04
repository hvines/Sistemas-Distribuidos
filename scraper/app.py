import requests  # type: ignore
import json
import os
import time
from pymongo import MongoClient, errors, ASCENDING  # type: ignore
from datetime import datetime
from redis import Redis  # type: ignore

redis_host = os.environ.get("REDIS_HOST", "redis")
cache = Redis(host=redis_host, port=6379, db=0)


mongo_uri = os.environ.get("MONGO_URI")
if not mongo_uri:
    raise ValueError("La variable de entorno MONGO_URI no está definida.")

client = MongoClient(mongo_uri)
db = client["waze_alertas"]
coleccion = db["eventos"]



# Limpiar la colección al inicio

result = coleccion.delete_many({})
print(f"Documentos eliminados al inicio: {result.deleted_count}", flush=True)



if "uuid_1" not in coleccion.index_information():
    coleccion.create_index([("uuid", ASCENDING)], unique=True, sparse=True)


def job():
    try:
        print("Descargando y procesando datos...", flush=True)

        url = (
            "https://www.waze.com/live-map/api/georss?"
            "top=-33.3464&bottom=-33.5121&"
            "left=-70.7404&right=-70.5459&"
            "env=row&types=alerts,traffic"
        )

        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"Error HTTP {resp.status_code}", flush=True)
            return  

        data = resp.json()
        alerts = data.get("alerts", [])
        print(f"Eventos descargados: {len(alerts)}", flush=True)

        insertados = 0
        for alert in alerts:
            alert["timestamp"] = datetime.utcnow()
            try:
                coleccion.insert_one(alert)
                insertados += 1
            except errors.DuplicateKeyError:
                pass

  
        cache.setex("latest_alerts", 10, json.dumps(alerts, default=str))
        print("Caché en latest_alerts de Redis por 10s", flush=True)

    except Exception as e:
        print(f"Error en la iteración: {e}", flush=True)


if __name__ == '__main__':
    while True:
        job()
        print("Esperando 1 segundo para más eventos...\n", flush=True)
        time.sleep(1)
