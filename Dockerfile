# AI-Driven Topo-Architect — Python 3.10 for Qiskit Metal compatibility
FROM python:3.10-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./topo_architect/

ENV PYTHONPATH=/app
ENV TOPO_API_URL=http://127.0.0.1:8000/api/v1

EXPOSE 8000 8501

CMD ["uvicorn", "topo_architect.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
