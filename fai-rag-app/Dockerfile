# Stage 1: Build the frontend
FROM node:16-bullseye as frontend-builder

WORKDIR /app/fai-frontend

# Copy frontend package.json and package-lock.json
COPY fai-frontend/package*.json ./

# Install frontend dependencies
RUN npm install

# Copy the rest of the frontend source code
COPY fai-frontend/ .

# Copy & make backend directory available for tailwindcss preprocessing
COPY fai-backend/fai_backend ./src/fai_backend

# Build the frontend
RUN npm run build

# Clean up backend directory
RUN rm -rf ./src/fai_backend

# Stage 2: Set up the backend
FROM python:3.11-bullseye

WORKDIR /app

# Copy the backend code and the built frontend from the first stage
COPY --from=frontend-builder /app/fai-frontend/dist ./fai-frontend/dist
COPY fai-backend/ ./fai-backend/
COPY pyproject.toml poetry.lock* ./

# Install poetry and backend dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

# Set environment variables for FastAPI
ENV HOST=0.0.0.0
ENV PORT=80

# Copy frontend build to static directory
RUN cp -r ./fai-frontend/dist ./fai-backend/fai_backend/static

# Clean up frontend files
RUN rm -rf ./fai-frontend

WORKDIR /app/fai-backend

# Command to run the FastAPI application
CMD uvicorn fai_backend.main:app --host $HOST --port $PORT