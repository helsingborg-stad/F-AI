# Stage: Get the git revision
FROM alpine/git AS git-revision
WORKDIR /tmp
RUN git ls-remote --heads https://github.com/helsingborg-stad/F-AI.git master | awk '{print substr($1, 1, 7)}' > git_revision.txt


# Stage: Build requirements for the backend
FROM python:3.11.9-slim-bookworm AS requirements-stage

WORKDIR /tmp

RUN pip install poetry && pip install poetry-plugin-export

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry export -f requirements.txt -o requirements.txt --without-hashes


# Stage: Build the final image with the backend and the frontend
FROM python:3.11.9-slim-bookworm
LABEL org.opencontainers.image.source=https://github.com/helsingborg-stad/F-AI

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  libmagic1 \
  libgl1 \
  libgl1-mesa-glx \
  libglib2.0-0

# Needed for images and PDFs.
RUN apt-get install -y --no-install-recommends \
  poppler-utils \
  tesseract-ocr

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
COPY --from=git-revision /tmp/git_revision.txt .

EXPOSE 8000

CMD ["fastapi", "run", "--proxy-headers", "main.py"]