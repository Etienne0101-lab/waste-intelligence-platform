FROM grafana/grafana:latest

COPY cloud-platform/dashboards/grafana/provisioning /etc/grafana/provisioning

EXPOSE 3000
