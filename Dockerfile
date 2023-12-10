FROM python:3.12-slim

# Install necessary tools for adding Microsoft's repository
RUN apt-get update \
    && apt-get install -y --no-install-recommends gnupg2 curl

# Add Microsoft's repository for the ODBC Driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install UnixODBC and Microsoft ODBC Driver for SQL Server
RUN apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends unixodbc-dev msodbcsql17

# Clean up the apt cache to reduce image size
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY ./sqlconnect ./sqlconnect
COPY ./tests ./tests

RUN chmod +x ./tests/integration/setup/docker-entrypoint.sh

CMD ["python", "-m", "pytest"]
