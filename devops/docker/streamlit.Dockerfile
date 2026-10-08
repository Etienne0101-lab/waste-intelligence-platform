FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "cloud-platform/dashboards/streamlit/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
