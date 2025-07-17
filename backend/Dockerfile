# ./backend/Dockerfile
# Dockerfile to create the container image for the FastAPI backend.

# Use a newer, supported Python runtime as a parent image (Bookworm instead of Buster)
FROM python:3.9-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# The 'pymysql' library specified in requirements.txt is pure Python and does not
# require system-level build tools like gcc. Therefore, the 'apt-get install'
# step is not needed, simplifying the Dockerfile and speeding up the build.

# Copy the requirements file into the container
# This is done first to leverage Docker's layer caching.
COPY ./requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ./app .

# Command to run the application using Uvicorn
# The command is changed from "app.main:app" to "main:app" because
# the WORKDIR is now the 'app' module itself.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]