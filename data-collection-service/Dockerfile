# Use an official Python runtime as a parent image
FROM python:3.11.9-bookworm

# Set the working directory in the container to /app
WORKDIR /app

# Add current directory contents to the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run data-collection-service.py when the container launches
CMD ["python", "data-collection-service.py"]