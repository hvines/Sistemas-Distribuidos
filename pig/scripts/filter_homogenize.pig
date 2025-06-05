-- pig/scripts/filter_homogenize.pig

-- 1. Cargar el CSV (suponemos que usa coma como separador y hay header)
events_raw = LOAD '/data/raw/events.csv'
    USING PigStorage(',', 'skipHeader=true')
    AS (campo1:chararray, campo2:chararray, campo3:chararray);

-- 2. Filtrar por algún parámetro. Por ejemplo, campo1 == 'valorX'
events_filtered = FILTER events_raw BY campo1 == 'valorX';

-- 3. (Opcional) Si quieres aplicar alguna homologación o transformación, agrégala aquí.

-- 4. Guardar el resultado en CSV en /data/processed/events_filtered.csv
STORE events_filtered
    INTO '/data/processed/events_filtered'
    USING PigStorage(',');