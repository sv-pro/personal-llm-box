FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

# Configure git to avoid permission issues with mounted volumes
RUN git config --global --add safe.directory /knowledge && \
    git config --global user.email "box@local" && \
    git config --global user.name "Personal AI Box"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY web-ui/ ./web-ui/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
