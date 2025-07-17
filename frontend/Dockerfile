# Use an official node image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy local files to the container
COPY . .

# The command to run the app is in docker-compose.yml
# This allows for using the dev server with hot-reloading
EXPOSE 5173

