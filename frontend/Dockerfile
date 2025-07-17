# Use an official Node runtime as a parent image for a single-stage build
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
# This takes advantage of Docker's layer caching, speeding up future builds
COPY package*.json ./

# Install all project dependencies, including 'vite'
RUN npm install

# Copy the rest of the frontend application code into the container.
# This will be overwritten by the volume mount in docker-compose for local development,
# but it's good practice for making the image self-contained.
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# The command to run the app is specified in docker-compose.yml.
# We can add a default CMD here for completeness, though it will be overridden.
CMD ["npm", "run", "dev"]