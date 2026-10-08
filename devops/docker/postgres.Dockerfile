FROM timescale/timescaledb:latest-pg15

RUN apt-get update && apt-get install -y postgresql-contrib && rm -rf /var/lib/apt/lists/*

COPY hub-layer/database/migrations/*.sql /docker-entrypoint-initdb.d/

ENV POSTGRES_DB=waste
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

EXPOSE 5432
