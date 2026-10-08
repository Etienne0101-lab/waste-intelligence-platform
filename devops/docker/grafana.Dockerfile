FROM grafana/grafana:latest

COPY cloud-platform/dashboards/grafana/provisioning/datasources.yaml /etc/grafana/provisioning/datasources/datasources.yaml
COPY cloud-platform/dashboards/grafana/provisioning/dashboards.yaml /etc/grafana/provisioning/dashboards/dashboards.yaml
COPY cloud-platform/dashboards/grafana/provisioning/alerts.yaml /etc/grafana/provisioning/alerts/alerts.yaml

EXPOSE 3000
