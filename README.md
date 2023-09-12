# F-AI: Helsingborg Language Model Exploration

## Project Overview

This repository contains a collection of Jupyter notebooks and Python scripts that explore the possibilities of applying large language models to common tasks for the city of Helsingborg.

## Goals

The current goal of this project is to create a framework that educates us and provides insights into what is possible and not possible to solve using language models.

## Running Docker with Docker Compose

To run this project using Docker and Docker Compose, follow these steps:

1. Ensure Docker and Docker Compose are installed on your machine. If not, you can download them from the [official Docker website](https://docs.docker.com/get-docker/).

2. Navigate to the project directory in your terminal.

3. Build the Docker image using the following command:
   ```
   docker-compose build
   ```
4. Once the image is built, run the Docker container using the following command:
   ```
   docker-compose up
   ```
5. The application should now be running on your specified port (default is 8888).

Please note that any changes made to the codebase will require a rebuild of the Docker image for the changes to take effect.

## Contribution Guidelines

We welcome contributions from the community! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch with a descriptive name.
3. Make your changes and commit them to your branch.
4. Submit a pull request to the main repository.

## License

This project is licensed under the MIT License.