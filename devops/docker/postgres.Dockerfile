FROM timescale/timescaledb:latest-pg15

RUN apt-get update && apt-get install -y postgresql-contrib && rm -rf /var/lib/apt/lists/*

COPY hub-layer/database/migrations/*.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
