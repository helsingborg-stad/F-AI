# Folkets AI Backend

This is the backend used to run Folkets AI. It exposes an HTTP API that can be used to
manage and handle LLM inference, chat conversations, assistants, permissions etc.

It is written in Python using FastAPI.

# Getting Started

The backend uses Poetry for dependency management. Make sure you have the correct Python
version and Poetry installed (see [pyproject.toml](pyproject.toml)). Then run `poetry install`.

# Running

Copy `.env.example` to `.env` and edit it to match your environment. A running MongoDB server is required.

Run the following command:

```shell
poetry run uvicorn main:app_instance
```

A server will start and listen on localhost. You can now go to
[http://localhost:8000/docs](http://localhost:8000/docs) to explore the API.

## Development

For convenience, you can also run `poetry run python main.py` or configure your IDE to run
main.py, which will start the server pre-configured with hot-reload.

# Tests

Test can be run with `./run_tests.sh`.

Implementations using MongoDB are not included in the default tests and can instead
be run using `./run_mongo_tests.sh`. This requires an active MongoDB server running on
`localhost` (recommended __not__ to use a production server as data could be lost).

# Feature Overview

This backend supports the following features:

* Run LLM inference against OpenAI-compatible servers
* Semantically chunk content of files and URLs
* Create and query vector embeddings
* Manage LLM assistants
* Manage chat conversations
* Usage through bearer tokens and/or API keys

## Auth

Most features are restricted behind "scopes" granted to groups. A user or API key
is then added to one or more groups in order to be granted these scopes (for example
the `chat` scope to be able to run chat with assistants).

To manage users, groups, and API keys, see the corresponding endpoints in the OpenAPI docs
([http://localhost:8000/docs](http://localhost:8000/docs)).