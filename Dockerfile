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
RUN npm run build && \
    echo "Contents of build directory:" && \
    ls -la build/

# Production stage
FROM nginx:stable

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copy Python requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create nginx directories and set permissions
RUN mkdir -p /var/log/nginx /var/cache/nginx /var/run && \
    chmod -R 777 /var/log/nginx /var/cache/nginx /var/run

# Copy built app and set permissions
COPY --from=builder /app/build /usr/share/nginx/html
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html && \
    echo "Contents of nginx html directory:" && \
    ls -la /usr/share/nginx/html

# Copy bot files
COPY bot.py ./
COPY start.sh ./

# Make start script executable
RUN chmod +x /app/start.sh

# Expose ports
EXPOSE 8080 3000

# Start both services
CMD ["/app/start.sh"] 