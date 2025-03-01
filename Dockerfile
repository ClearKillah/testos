# Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy project files
COPY . .

# Build the app
RUN npm run build

# Production stage
FROM nginx:stable

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built app
COPY --from=builder /app/build /usr/share/nginx/html

# Copy bot files
COPY bot.py /app/
COPY start.sh /app/

# Make start script executable
RUN chmod +x /app/start.sh

# Expose port
EXPOSE 8080 3000

# Start both services
CMD ["/app/start.sh"] 