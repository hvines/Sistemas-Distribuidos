-- pig/filter_homogenize.pig
-- --------------------------------------------------------
-- 1) Registrar Piggybank para JsonLoader/JsonStorage
-- 2) Cargar JSON exportado desde Mongo (una línea = un documento JSON)
-- 3) Filtrar registros incompletos
-- 4) Homogeneizar campos (type, comuna, timestamp)
-- 5) Eliminar duplicados exactos
-- 6) Agrupar por comuna (conteo total)
-- 7) Guardar stats_by_commune.csv
-- 8) Agrupar por (comuna, fecha) para evolución temporal
-- 9) Guardar freq_evolution.csv
-- --------------------------------------------------------

-- 1) Registrar piggybank.jar
REGISTER /usr/local/pig/piggybank.jar;

-- 2) Cargar datos
raw_events = 
    LOAD '/data/raw/events.json'
    USING org.apache.pig.piggybank.storage.JsonLoader(
      'type:chararray, comuna:chararray, timestamp:chararray, coords:map[], other:map[]'
    )
    AS (type:chararray, comuna:chararray, timestamp:chararray, coords:map[], other:map[]);

-- 3) Filtrar registros con campos nulos o vacíos
filtered_events = 
    FILTER raw_events BY 
      (type IS NOT NULL AND comuna IS NOT NULL AND timestamp IS NOT NULL 
       AND type != '' AND comuna != '' AND timestamp != '');

-- 4) Homogeneizar campos principales
normalized = 
    FOREACH filtered_events GENERATE
      UPPER(type)                     AS type_norm,
      LOWER(comuna)                   AS comuna_norm,
      ToDate(timestamp, 'yyyy-MM-dd''T''HH:mm:ss') AS ts,
      coords                           AS coords,
      other                            AS other;

-- 5) Eliminar duplicados exactos tras normalizar
distinct_events = DISTINCT normalized;

-- 6) Agrupar por comuna para conteo total de incidentes
group_commune = GROUP distinct_events BY comuna_norm;

stats_by_commune = 
    FOREACH group_commune GENERATE
      group             AS comuna, 
      COUNT(distinct_events) AS total_incidents;

-- 7) Guardar stats_by_commune (comuna,total_incidents) en CSV
STORE stats_by_commune 
  INTO '/data/processed/stats_by_commune.csv' 
  USING PigStorage(',');

-- 8) Preparar datos para evolución temporal diaria
events_with_date = 
    FOREACH distinct_events GENERATE
      comuna_norm, 
      ToString(ts, 'yyyy-MM-dd') AS date_str;

group_commune_date = GROUP events_with_date BY (comuna_norm, date_str);

freq_evolution = 
    FOREACH group_commune_date GENERATE
      FLATTEN(group)           AS (comuna, date), 
      COUNT(events_with_date)  AS count_per_day;

-- 9) Guardar freq_evolution (comuna,date,count_per_day) en CSV
STORE freq_evolution 
  INTO '/data/processed/freq_evolution.csv' 
  USING PigStorage(',');

-- FIN del script