# NCBiR backend

The repository contains a backend to the web application for the NCBiR project

## Requirements
- Docker :whale:
- Docker-Compose :whale:

## Quick Start
Use make to and run docker:

Create file .env with env vars (if not make will do it based on .env-template), then just call

```bash
make run 
```

or you can just call docker-compose
```bash
cp .env-template .env
docker-compose up -d 
```

## Setup environment (make)
```bash
make install
```

## Setup environment (manual)
```bash
python -m venv .venv
source .venv/bin/active
pip install -r requirements.txt -r requirements-dev.txt
cp .env-template .env
```



## Usage
After creating the container, the swagger will be available at:
http://localhost/api/v1/docs

Port can be assign in .env file (default is 5050)

## Make command list
- install: setup environment
- lint: run linters 
- clean: remove cache files and dirs from local env
- run: run container
- test: run tests
