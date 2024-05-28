# Stage 1: Build the frontend
FROM node:16 as frontend-builder

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
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg libsm6 libxext6 libmagic1

# Install poetry for dependency management
RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set the working directory
WORKDIR /app

# Copy the backend dependencies files
COPY fai-backend/pyproject.toml fai-backend/poetry.lock ./

# Install backend dependencies
RUN poetry install
RUN rm -rf $POETRY_CACHE_DIR

# Copy the backend source code
COPY fai-backend/fai_backend ./fai_backend

# Copy the frontend build from the frontend-builder stage
COPY --from=frontend-builder /app/fai-frontend/dist ./fai_backend/static
RUN rm -rf /app/fai-frontend

# Set environment variables for FastAPI
ENV HOST=0.0.0.0
ENV PORT=80

# Command to run the FastAPI application
CMD uvicorn fai_backend.main:app --host $HOST --port $PORT