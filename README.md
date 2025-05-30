docker-compose up --build -d waze-scraper

localhost:8081 ---> mongoDB

- Se inicia el scraper
docker-compose up --build -d

- Scraper empieza y a cada segundo agrega a mongoDB 200 eventos
    Para comprobar: docker-compose logs -f waze-scraper
- Dejar andando por 50 segundos mínimo para llenar dB con 10.000 eventos

- Al dejar andando el scraper, REDIS como sistema de caché empieza a funcionar
    localhost:8082


    