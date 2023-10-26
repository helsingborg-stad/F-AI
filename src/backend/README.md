# F-AI: FastAPI Backend
This is the backend service for the F-AI project, built using FastAPI.

## Requirements
- Python 3.11.0 or higher is required
- MongoDB

## Getting started
1. Set up a virtual environment: 
   ```shell
   python3 -m venv venv
   ```
2. Activate the virtual environment: 
   ```shell
   source venv/bin/activate
   ```
3. Navigate to the backend directory: 
   ```shell
   cd src/backend
   ```
4. Install the required packages: 
   ```shell
   pip install -r requirements.txt
   ```
5. Run the application: 
   ```shell
   python main.py
   ```
6. Access the local instance at: 
   http://127.0.0.1:8000

## API Documentation
FastAPI generates interactive API documentation. You can access them at:
1. Swagger: http://127.0.0.1:8000/docs
2. Redoc: http://127.0.0.1:8000/redoc
3. The OpenAPI JSON schema is available at: http://127.0.0.1:8000/openapi.json

## Dependencies
- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- [Pydantic](https://pydantic-docs.helpmanual.io/): Data validation and settings management using Python type annotations.
- [Beanie](https://roman-right.github.io/beanie/): An asynchronous Python object-document mapper (ODM) for MongoDB, built on top of Motor and Pydantic.
- [Motor](https://motor.readthedocs.io/): The async Python driver for MongoDB.
- [MongoDB](https://www.mongodb.com/): A source-available cross-platform document-oriented database program.

## Application Structure
```
src/backend/
    ├── main.py # Entry point of the application.
    ├── app/ # Contains application configuration and initialization code.
    ├── db/ # Handles the database operations.
    ├── schema/ # API schema type definitions.
    ├── api/ # Defines the API routes and handlers.
    └── service/ # Contains the business logic of the application.
```
