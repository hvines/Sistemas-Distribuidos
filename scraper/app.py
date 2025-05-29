import requests
import json
import os
import time
from pymongo import MongoClient

# Conexión a MongoDB
print("🚀 Iniciando scraper...")
mongo_uri = os.environ.get("MONGO_URI")
if not mongo_uri:
    raise ValueError("❌ La variable de entorno MONGO_URI no está definida.")
client = MongoClient(mongo_uri)

# Configuración de base de datos
db_name = "waze_alertas"
collection_name = "eventos"
db = client[db_name]
coleccion = db[collection_name]

# Bucle principal
while True:
    try:
        print("🛰️  Descargando y procesando datos...")

        url = (
            "https://www.waze.com/live-map/api/georss?"
            "top=-33.3464&bottom=-33.5121&"
            "left=-70.7404&right=-70.5459&"
            "env=row&types=alerts,traffic"
        )

        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}")
            continue

        data = json.loads(response.text)
        alerts = data.get("alerts", [])

        print(f"📦 Alertas descargadas: {len(alerts)}")

        if alerts:
            if collection_name in db.list_collection_names():
                print("♻️ Limpiando colección anterior...")
                coleccion.delete_many({})
            else:
                print(f"🆕 Creando colección '{collection_name}'...")

            coleccion.insert_many(alerts)
            print(f"✅ Se insertaron {len(alerts)} documentos en MongoDB.")
        else:
            print("⚠️ No se encontraron alertas para insertar. No se modifica la colección.")

    except Exception as e:
        print(f"🔥 Error general en la iteración: {e}")

    print("⏳ Esperando 10 minutos para la próxima actualización...\n")
    time.sleep(600)