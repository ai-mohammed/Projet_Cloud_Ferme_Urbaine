# Python 3.11.9
FROM python:3.11.9-bookworm

# Set working directory to /app
WORKDIR /app

# Add current directory to /app
ADD . /app

ENV DB_HOST=host.docker.internal
ENV DB_PORT=5432
ENV DB_NAME=Urban_Farm_Monitoring
ENV DB_USER=admin
ENV DB_PASS=adminXDD


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available
EXPOSE 80

# Run models.py
CMD ["python", "models.py"]