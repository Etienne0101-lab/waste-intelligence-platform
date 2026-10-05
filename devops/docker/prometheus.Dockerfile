FROM prom/prometheus:latest

COPY devops/monitoring/prometheus.yml /etc/prometheus/prometheus.yml

EXPOSE 9090
