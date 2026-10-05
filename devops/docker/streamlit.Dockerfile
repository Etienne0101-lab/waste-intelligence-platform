FROM python:3.11-slim

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir streamlit

EXPOSE 8501

CMD ["streamlit", "run", "cloud-platform/dashboards/streamlit/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
