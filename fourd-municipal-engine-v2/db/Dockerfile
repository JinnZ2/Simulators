FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PostGIS C-libraries & compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY db/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY fourd_municipal_engine/ ./fourd_municipal_engine/

EXPOSE 8000

CMD ["uvicorn", "fourd_municipal_engine.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
