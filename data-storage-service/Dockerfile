# Use an official PostgreSQL runtime as a parent image
FROM postgres:latest

# Set the working directory in the container to /docker-entrypoint-initdb.d
WORKDIR /docker-entrypoint-initdb.d

# Add init.sql to the docker-entrypoint-initdb.d directory
ADD init.sql /docker-entrypoint-initdb.d

# Run the SQL commands in init.sql when the container starts
CMD ["postgres"]