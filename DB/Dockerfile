# Use the official image as a parent image
FROM postgres:latest

# Set environment variables
ENV POSTGRES_DB=pipeline_pundits_db
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=r00t

# When the container starts, this script will run and set up your database
COPY setup.sql /docker-entrypoint-initdb.d/

# The default port for PostgreSQL is 5432
EXPOSE 5432
