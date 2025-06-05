# pig/Dockerfile

FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

# 1. Instalar Java (para Pig), Python y utilidades
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk python3 python3-pip wget gnupg && \
    rm -rf /var/lib/apt/lists/*

# 2. Instalar Apache Pig (versión 0.17.0, por ejemplo)
WORKDIR /opt
RUN wget https://archive.apache.org/dist/pig/pig-0.17.0/pig-0.17.0.tar.gz && \
    tar -xzvf pig-0.17.0.tar.gz && \
    mv pig-0.17.0 pig && \
    rm pig-0.17.0.tar.gz

# 3. Configurar variables de entorno para Pig
ENV PIG_HOME=/opt/pig
ENV PATH=$PIG_HOME/bin:$PATH

# 4. Instalar pymongo (Python)
RUN pip3 install pymongo

# 5. Crear directorios fijos para volúmenes
RUN mkdir -p /data/raw /data/processed /scripts

# 6. Copiar scripts de Python y Pig Latin
COPY scripts/export_data.py /scripts/export_data.py
COPY scripts/filter_homogenize.pig /scripts/filter_homogenize.pig

# 7. Marcar /scripts/ como ejecutable (no es obligatorio)
RUN chmod +x /scripts/export_data.py

# 8. Copiar requirements.txt si tuvieras más dependencias (opcional)
# COPY requirements.txt /scripts/requirements.txt
# RUN pip3 install -r /scripts/requirements.txt

WORKDIR /scripts

# 9. Configurar un entrypoint que repita periodicidad
ENTRYPOINT [ "bash", "-c" ]
CMD [ "\
  while true; do \
    echo \"[pig] Iniciando exportación a CSV desde MongoDB...\"; \
    python3 /scripts/export_data.py || { echo \"[pig] Error en export_data.py\"; sleep 10; continue; }; \
    echo \"[pig] CSV generado, ejecutando Pig Latin...\"; \
    pig -x local /scripts/filter_homogenize.pig || { echo \"[pig] Error en Pig Latin\"; sleep 10; continue; }; \
    echo \"[pig] Pig terminó, datos en /data/processed\"; \
    echo \"[pig] Durmiendo 30s antes de próxima iteración...\"; \
    sleep 30; \
  done\
" ]