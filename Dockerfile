# Build stage for React app
FROM node:18-alpine as react-build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Build the app
RUN npm run build

# Production stage
FROM python:3.9-slim

WORKDIR /app

# Copy Python requirements and bot
COPY requirements.txt bot.py ./

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy built React app from build stage
COPY --from=react-build /app/build ./static

# Expose port
EXPOSE 8080

# Start command
CMD ["python", "bot.py"] 