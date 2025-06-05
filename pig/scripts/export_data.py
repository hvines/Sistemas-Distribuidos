# pig/scripts/export_data.py

import os
import csv
from pymongo import MongoClient

def export_to_csv():
    # Obtener URI de Mongo (use authSource=admin si aplica)
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://root:example@mongodb:27017/?authSource=admin")
    
    # Nombre de la base y colección (ajusta según tu caso real)
    db_name = os.environ.get("MONGO_DBNAME", "tu_base")
    coll_name = os.environ.get("MONGO_COLLNAME", "tu_coleccion")

    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[coll_name]

    # Abrir CSV para escritura. 
    # Cada vez lo sobreescribe, generando un CSV limpio.
    output_path = "/data/raw/events.csv"
    with open(output_path, mode="w", newline="", encoding="utf-8") as csvfile:
        # Ajusta los campos que quieres extraer:
        fieldnames = ["campo1", "campo2", "campo3"]  # reemplaza por los nombres reales
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Recorremos todos los documentos
        cursor = collection.find({}, {fn: 1 for fn in fieldnames})  # sólo esos campos
        for doc in cursor:
            # Asegúrate de llenar cada campo; si falta, deja vacío
            row = {fn: doc.get(fn, "") for fn in fieldnames}
            writer.writerow(row)

    print(f"[export_data.py] CSV escrito en {output_path}")

if __name__ == "__main__":
    export_to_csv()