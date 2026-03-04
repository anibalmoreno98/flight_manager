FROM python:3.12

# set working dir at root of project inside container
WORKDIR /app

# install deps early so we can leverage layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the application code; will be overridden by a volume mount in development
COPY app ./app

# run the server pointing at the correct module and enable reload on /app
# use reload-dir to make sure the watcher sees changes inside the mounted volume
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app"]
