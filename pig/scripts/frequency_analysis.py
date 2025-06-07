import os
import csv
from pymongo import MongoClient
import sys
from datetime import datetime

def analyze_frequency():
    """Función para analizar la frecuencia de ocurrencia de diferentes tipos de incidentes"""
    print("=== ANÁLISIS DE FRECUENCIA DE INCIDENTES ===")
    
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://root:example@mongodb:27017/?authSource=admin")
    db_name = os.environ.get("MONGO_DBNAME", "waze_alertas")
    coll_name = os.environ.get("MONGO_COLLNAME", "eventos")
    
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[coll_name]
        
        # Verificar conexión total
        total_docs = collection.count_documents({})
        print(f"Total documentos en la colección: {total_docs}")
        
        if total_docs == 0:
            print("⚠️  No hay documentos en la colección")
            return

        print("Analizando frecuencia de tipos de incidentes...")
        
        # Análisis por tipo de incidente
        type_pipeline = [
            {"$group": {"_id": "$type", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        # Análisis por ciudad
        city_pipeline = [
            {"$group": {"_id": "$city", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        # Análisis combinado: tipo por ciudad
        combined_pipeline = [
            {"$group": {"_id": {"type": "$type", "city": "$city"}, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        # Ejecutar análisis
        type_results = list(collection.aggregate(type_pipeline))
        city_results = list(collection.aggregate(city_pipeline))
        combined_results = list(collection.aggregate(combined_pipeline))
        
        # Crear archivo CSV de frecuencia por tipo
        output_path_type = "/scripts/frecuencia_por_tipo.csv"
        print(f"Exportando frecuencia por tipo a: {output_path_type}")
        
        with open(output_path_type, mode="w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["tipo", "cantidad", "porcentaje"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for result in type_results:
                event_type = result["_id"]
                count = result["count"]
                percentage = (count / total_docs) * 100
                
                row = {
                    "tipo": event_type,
                    "cantidad": count,
                    "porcentaje": f"{percentage:.2f}%"
                }
                writer.writerow(row)
        
        # Crear archivo CSV de frecuencia por ciudad
        output_path_city = "/scripts/frecuencia_por_ciudad.csv"
        print(f"Exportando frecuencia por ciudad a: {output_path_city}")
        
        with open(output_path_city, mode="w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["ciudad", "cantidad", "porcentaje"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for result in city_results:
                city = result["_id"]
                count = result["count"]
                percentage = (count / total_docs) * 100
                
                row = {
                    "ciudad": city,
                    "cantidad": count,
                    "porcentaje": f"{percentage:.2f}%"
                }
                writer.writerow(row)
        
        # Crear archivo CSV combinado
        output_path_combined = "/scripts/frecuencia_tipo_ciudad.csv"
        print(f"Exportando frecuencia combinada a: {output_path_combined}")
        
        with open(output_path_combined, mode="w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["tipo", "ciudad", "cantidad", "porcentaje"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for result in combined_results:
                event_type = result["_id"]["type"]
                city = result["_id"]["city"]
                count = result["count"]
                percentage = (count / total_docs) * 100
                
                row = {
                    "tipo": event_type,
                    "ciudad": city,
                    "cantidad": count,
                    "porcentaje": f"{percentage:.2f}%"
                }
                writer.writerow(row)
        
        # Mostrar resumen en consola
        print(f"\n=== RESUMEN DE FRECUENCIAS ===")
        print(f"Total de eventos analizados: {total_docs}")
        
        print(f"\n📊 TOP 5 TIPOS DE INCIDENTES:")
        for i, result in enumerate(type_results[:5], 1):
            event_type = result["_id"]
            count = result["count"]
            percentage = (count / total_docs) * 100
            print(f"  {i}. {event_type}: {count} eventos ({percentage:.2f}%)")
        
        print(f"\n🏙️  TOP 5 CIUDADES CON MÁS INCIDENTES:")
        for i, result in enumerate(city_results[:5], 1):
            city = result["_id"]
            count = result["count"]
            percentage = (count / total_docs) * 100
            print(f"  {i}. {city}: {count} eventos ({percentage:.2f}%)")
        
        print(f"\n🔥 TOP 5 COMBINACIONES TIPO-CIUDAD:")
        for i, result in enumerate(combined_results[:5], 1):
            event_type = result["_id"]["type"]
            city = result["_id"]["city"]
            count = result["count"]
            percentage = (count / total_docs) * 100
            print(f"  {i}. {event_type} en {city}: {count} eventos ({percentage:.2f}%)")
        
        print(f"\n✅ Archivos de frecuencia exportados:")
        print(f"  - {output_path_type}")
        print(f"  - {output_path_city}")
        print(f"  - {output_path_combined}")
        
        return len(type_results)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0

def analyze_frequency_by_type(event_type):
    """Función para analizar la frecuencia de un tipo específico por ciudad"""
    print(f"=== ANÁLISIS DE FRECUENCIA PARA TIPO: {event_type} ===")
    
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://root:example@mongodb:27017/?authSource=admin")
    db_name = os.environ.get("MONGO_DBNAME", "waze_alertas")
    coll_name = os.environ.get("MONGO_COLLNAME", "eventos")
    
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[coll_name]
        
        # Filtrar por tipo específico
        query = {"type": {"$regex": f"^{event_type}$", "$options": "i"}}
        
        # Contar total de este tipo
        total_type = collection.count_documents(query)
        print(f"Total eventos de tipo '{event_type}': {total_type}")
        
        if total_type == 0:
            print(f"⚠️  No se encontraron eventos de tipo '{event_type}'")
            return
        
        # Análisis por ciudad para este tipo
        pipeline = [
            {"$match": query},
            {"$group": {"_id": "$city", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        results = list(collection.aggregate(pipeline))
        
        # Crear archivo CSV
        output_path = f"/scripts/frecuencia_{event_type.lower()}_por_ciudad.csv"
        print(f"Exportando a: {output_path}")
        
        with open(output_path, mode="w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["ciudad", "cantidad", "porcentaje"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for result in results:
                city = result["_id"]
                count = result["count"]
                percentage = (count / total_type) * 100
                
                row = {
                    "ciudad": city,
                    "cantidad": count,
                    "porcentaje": f"{percentage:.2f}%"
                }
                writer.writerow(row)
        
        # Mostrar resumen
        print(f"\n📊 DISTRIBUCIÓN DE {event_type} POR CIUDAD:")
        for i, result in enumerate(results, 1):
            city = result["_id"]
            count = result["count"]
            percentage = (count / total_type) * 100
            print(f"  {i}. {city}: {count} eventos ({percentage:.2f}%)")
        
        print(f"\n✅ Archivo exportado: {output_path}")
        return len(results)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        event_type = sys.argv[1]
        analyze_frequency_by_type(event_type)
    else:
        print("Uso:")
        print("  python3 frequency_analysis.py           # Análisis general de frecuencias")
        print("  python3 frequency_analysis.py JAM       # Análisis de frecuencia para tipo específico")
        print("")
        print("El script sin parámetros hace análisis completo de frecuencias")
        
        # Ejecutar análisis general por defecto
        analyze_frequency()