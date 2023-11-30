FROM python:3.12-slim

# Update package lists and install dependencies for pyodbc
RUN apt-get update \
    && apt-get install -y --no-install-recommends unixodbc-dev

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./sqlconnect ./sqlconnect
COPY ./tests ./tests

CMD ["python", "-m", "pytest"]