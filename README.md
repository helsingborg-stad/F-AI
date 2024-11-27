# Getting started

## Try it on Elastx

1. Sign up on Elastx <https://elastx.se/se/signup>
2. Click button

[![Install demo](https://raw.githubusercontent.com/helsingborg-stad/F-AI/5e0c8dcac95f2468b4509927ccc2f410c08b0508/.deploy/elastx/elastx_install_demo.png)](https://app.jelastic.elastx.net/?manifest=https://raw.githubusercontent.com/helsingborg-stad/F-AI/refs/heads/wip/1-click-install-elastx/.deploy/elastx/mainfest.yml)

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
cd F-AI/fai-rag-app/fai-backend
```

```bash
poetry shell && poetry install --with dev,test,unstructured
```

Setup mongodb as needed.

```bash
cp .env.example .env
```

Edit .env to fit your needs

```bash
python -m fai_backend.main
```

### Frontend 🎸

```bash
cd F-AI/fai-rag-app/fai-frontend
```

```bash
npm i
```

```bash
npm run dev
```

#### View in browser 🚀

```bash
open http://localhost:8000
```

##### API Docs

```bash
open http://localhost:8000/docs
```

##### API Root Endpoint 🤩

```bash
open http://localhost:8000/api
```
