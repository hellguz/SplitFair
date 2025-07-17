# Dockerfile for the FastAPI backend service.

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies that might be required
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of the backend application code into the container
COPY . /app

# The command to run the application will be specified in docker-compose.yml
# This allows for flexibility (e.g., running tests vs. running the server).
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
