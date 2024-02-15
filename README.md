# NCBiR backend

The repository contains a backend to the web application for the NCBiR project.


## Make setup
Check if make is already installed
```bash
make --version
```
If not, install make
```bash
sudo apt install make
```


## Make stages
Install virtual environment and all dependencies
```bash
make install
```
Run linters check (black, pylama)
```bash
make lint
```
Create a copy of env file, create and start docker containter defined in `docker-compose.yml`
```bash
make run
```
Stop and remove container
```bash
make down
```
Remove temporary files such as .venv, .mypy_cache, .pytest_cache etc.
```bash
make clean
```
Run unit tests (runs lint stage before)
```bash
make test
```
___

# Quick Start


## Run docker container
Ensure Docker has been installed before
```bash
make run
```


## Creating project environment
You can create virtual environment using make:
```bash
make install
```
or manually:
```bash
# Create and source virtual Environment
python -m venv .venv
source .venv/bin/active

# Install all requirements and dependencies
pip install .
pip install .[dev]

# Init pre-commit hook
pre-commit install
```


## Usage
After creating the container, the swagger will be available at:
http://localhost/api/v1/docs

Port can be assign in .env file (default is 5050)

