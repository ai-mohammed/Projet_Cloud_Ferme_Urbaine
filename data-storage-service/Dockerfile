# Python 3.12.2
FROM python:3.12.2-bookworm

# Set working directory to /app
WORKDIR /app

# Add current directory to /app
ADD . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available
EXPOSE 80

# Run models.py
CMD ["python", "models.py"]