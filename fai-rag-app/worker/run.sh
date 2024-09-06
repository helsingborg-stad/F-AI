#!/usr/bin/env bash

PROJECT_DIR="${PDW}"
DOCKER_COMPOSE_CMD="docker-compose -p fai-queue up"

cd "$PROJECT_DIR" || { echo "Failed to navigate to project directory"; exit 1; }

$DOCKER_COMPOSE_CMD
