# Getting started

## Development (macOS)

```bash
brew install libmagic
```

```bash
brew install python@3.11
```

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

```bash
git clone https://github.com/helsingborg-stad/F-AI.git
```

### Backend 🤖

```bash
cd F-AI/backend
```

```bash
poetry shell && poetry install --with dev,test,unstructured
```

```bash
cp .env.example .env
```

Edit .env to fit your needs

```bash
python -m fai_backend.main
```

### Frontend 🎸

The front-end is currently under development and not complete as we refactor the project. 

For a working version with both front-end and back-end functionality, switch to Git tag "0.0.34", for the last stable release.