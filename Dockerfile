# Build stage for React app
FROM node:18-alpine as react-build

# Увеличиваем память для Node
ENV NODE_OPTIONS=--max_old_space_size=4096

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with verbose logging
RUN npm install --legacy-peer-deps --verbose

# Copy project files
COPY . .

# Build the app with verbose output
RUN CI=false npm run build

# Production stage
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot file
COPY bot.py .

# Copy built React app from build stage
COPY --from=react-build /app/build ./static

# Expose port
EXPOSE 8080

# Start command
CMD ["python", "bot.py"] 