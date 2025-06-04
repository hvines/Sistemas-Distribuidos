# pig/Dockerfile
# --------------------------------------------------------
# 1) Imagen base Ubuntu 22.04 (puedes usar otra distro si prefieres)
# 2) Instalamos Java, wget, mongo-tools (mongoexport/mongoimport) y Pig
# 3) Creamos carpetas /scripts, /data/raw y /data/processed
# 4) Copiamos el script Pig
# --------------------------------------------------------

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PIG_HOME=/usr/local/pig
ENV PATH=$PIG_HOME/bin:$PATH

# 1) Instalar Java 11 (headless), wget, gnupg y mongo-tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      openjdk-11-jdk-headless \
      wget \
      gnupg \
      curl && \
    # Instalar MongoDB Database Tools para tener mongoexport y mongoimport
    wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add - && \
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" \
      | tee /etc/apt/sources.list.d/mongodb-org-6.0.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends mongodb-database-tools && \
    rm -rf /var/lib/apt/lists/*

# 2) Descargar e instalar Apache Pig 0.17.0 (ajusta la versión si lo deseas)
RUN wget https://archive.apache.org/dist/pig/pig-0.17.0/pig-0.17.0.tar.gz -O /tmp/pig.tar.gz && \
    mkdir -p $PIG_HOME && \
    tar -xzf /tmp/pig.tar.gz -C $PIG_HOME --strip-components=1 && \
    rm /tmp/pig.tar.gz

# 3) Crear directorios necesarios
RUN mkdir -p /scripts /data/raw /data/processed

# 4) Copiar el script Pig al contenedor
COPY filter_homogenize.pig /scripts/filter_homogenize.pig

# 5) (Opcional) Si en tu distribución de Pig no viene piggybank.jar,
#    cópialo manualmente aquí. De lo contrario, puedes comentar esta línea:
# COPY piggybank.jar $PIG_HOME/piggybank.jar

WORKDIR /scripts

# El ENTRYPOINT será bash; el comando real lo proveeremos en docker-compose.yml
ENTRYPOINT ["/bin/bash"]