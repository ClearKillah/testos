# Build stage for React app
FROM node:18-alpine as react-build

# Увеличиваем память для Node
ENV NODE_OPTIONS=--max_old_space_size=4096

WORKDIR /app

# Copy package files
COPY package*.json ./

# Clean npm cache and install dependencies
RUN npm cache clean --force && \
    rm -rf node_modules && \
    npm install --legacy-peer-deps --verbose && \
    npm install ajv@8.12.0 ajv-keywords@5.1.0 --save

# Copy project files
COPY . .

# Build the app
RUN CI=false npm run build

# Serve stage
FROM node:18-alpine

WORKDIR /app

# Install serve
RUN npm install -g serve

# Copy built app
COPY --from=react-build /app/build ./build

# Expose port
EXPOSE 8080

# Start command
CMD ["serve", "-s", "build", "-l", "8080"] 