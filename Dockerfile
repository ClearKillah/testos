# Build stage for React app
FROM node:18-alpine as react-build

WORKDIR /app/frontend

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Build the app
RUN npm run build

# Python stage
FROM python:3.9-slim

WORKDIR /app

# Copy Python requirements
COPY requirements.txt .
COPY bot.py .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy built React app
COPY --from=react-build /app/frontend/build ./frontend/build

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start command
CMD ["python", "bot.py"] 