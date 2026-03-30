FROM python:3.12

# set working dir at root of project inside container
WORKDIR /app

# install deps early so we can leverage layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the application code; will be overridden by a volume mount in development
COPY app ./app

# Expose FastAPI port
EXPOSE 8000

# Default command (docker-compose override will replace this in dev)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]