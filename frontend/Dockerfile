# ./frontend/Dockerfile
# Dockerfile to build the React frontend and serve it with Nginx.

# --- Stage 1: Build the React application ---
FROM node:18-alpine AS build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY . .

# Build the application for production
# VITE_API_BASE_URL is passed as a build-time argument from docker-compose
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build

# --- Stage 2: Serve the application with Nginx ---
FROM nginx:1.25-alpine

# Copy the built assets from the 'build' stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the Nginx configuration file
# This is needed to make client-side routing (React Router) work correctly.
# It tells Nginx to always serve index.html for any path that is not a file.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]

