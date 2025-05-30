import requests
import json
import os
import time
from pymongo import MongoClient, errors, ASCENDING
from datetime import datetime
from redis import Redis


redis_host = os.environ.get("REDIS_HOST", "redis")
cache = Redis(host=redis_host, port=6379, db=0)

# Inicia Scraper...
mongo_uri = os.environ.get("MONGO_URI")
if not mongo_uri:
    raise ValueError("La variable de entorno MONGO_URI no está definida.")

client = MongoClient(mongo_uri)
db = client["waze_alertas"]
coleccion = db["eventos"]



# ─── 1) BORRAR AL INICIO ─────────────────────────────────────
result = coleccion.delete_many({})
print(f"🗑️  Documentos eliminados al inicio: {result.deleted_count}", flush=True)

# ─── 2) INDICE ───────────────────────────────────────────────
if "uuid_1" not in coleccion.index_information():
    coleccion.create_index([("uuid", ASCENDING)], unique=True, sparse=True)

# Bucle principal
while True:
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
            time.sleep(10)
            continue

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

        # Cacheamos el último batch en Redis durante 10 segundos
        cache.setex("latest_alerts", 10, json.dumps(alerts, default=str))
        print("Cached latest_alerts en Redis por 10s", flush=True)

        print("Esperando 10 segundos…\n", flush=True)
        time.sleep(10)
        

    except Exception as e:
        print(f"Error en la iteración: {e}", flush=True)

    print("Esperando 1 segundo...\n", flush=True)
    time.sleep(1)