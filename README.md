# F-AI: Helsingborg Language Model Exploration

## Project Overview

This repository contains a collection of Jupyter notebooks and Python scripts that explore the possibilities of applying large language models to common tasks for the city of Helsingborg.

## Goals

The current goal of this project is to create a framework that educates us and provides insights into what is possible and not possible to solve using language models.

## Running with Docker locally

To run this project using Docker, follow these steps:

1. Ensure Docker are installed on your machine. If not, you can download them from the [official Docker website](https://docs.docker.com/get-docker/).

2. Navigate to the project directory in your terminal.

3. Build the Docker image using the following command:
   ```shell
   $ docker build -t f-ai-pp:local .
    
   # with --platform ⛳️ (apple silicon/m1):
   $ docker build --platform linux/amd64 -t f-ai-pp:local .
   ```
  
4. Once the image is built, run the Docker container using the following command:
   ```shell
   # for local development using docker (with mount and port 8001)
   $ docker run \
      --name f-ai-pp-local \
      -e CHAINLIT_PORT=8001 \
      -p 8001:8001 \
      -v "$(pwd)"/src/planning_permission/.env:/app/.env \
      -v "$(pwd)"/src/planning_permission/data:/app/data \
      -v "$(pwd)"/src/planning_permission:/app/planning_permission \
      --platform linux/amd64 \
      f-ai-pp:local
      
      # not a apple silicon/m1 user? remove the row 👆 with --platform ⛳️
   ```
5. The application should now be running on your specified port (8001 or 80).

Please note that any changes made to the codebase will require a rebuild of the Docker image for the changes to take effect.

## Analytics and Logging

We use Sentry for error tracking and performance monitoring to ensure the best user experience. Sentry provides real-time monitoring and detailed error reports, which help us detect, triage, and resolve issues faster.

By default, Sentry is **not enabled** in this project. If you wish to enable Sentry logging, ensure you've set the appropriate environment variables as described in the `.env.example` file.

Sentry is an open-source application monitoring platform that helps developers identify and fix crashes in real time. It provides detailed stack traces and environmental context for better issue resolution. For more information, visit [Sentry's official documentation](https://docs.sentry.io/).

## Contribution Guidelines

We welcome contributions from the community! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch with a descriptive name.
3. Make your changes and commit them to your branch.
4. Submit a pull request to the main repository.

## License

This project is licensed under the MIT License.