ifeq ($(OS),Windows_NT)
    VENV_ACTIVATE := .venv\Scripts\activate
else
    VENV_ACTIVATE := .venv/bin/activate
endif
CODE_DIRS := zefir_api tests

ifndef ENV_FILE_EXISTS
    ifeq ($(wildcard .env),)
        ENV_FILE_EXISTS := false
    else
        ENV_FILE_EXISTS := true
    endif
endif

.PHONY: install lint clean run down test

$(VENV_ACTIVATE): pyproject.toml .pre-commit-config.yaml
	python3.11 -m venv .venv
	. $(VENV_ACTIVATE) && pip install --upgrade pip \
		&& pip install . \
		&& pip install .[dev]
	. $(VENV_ACTIVATE) && pre-commit install

install: $(VENV_ACTIVATE)

lint: $(VENV_ACTIVATE)
	. $(VENV_ACTIVATE) && black $(CODE_DIRS) \
		&& pylama -l mccabe,pycodestyle,pyflakes,radon,mypy $(CODE_DIRS) --async --skip=.*/*

clean:
	rm -rf $(VENV_ACTIVATE) .mypy_cache .pytest_cache .tox
	find . | grep -E "(/__pycache__$$|\.pyc$|\.pyo$$)" | xargs rm -rf

run:
	@if [ "$(ENV_FILE_EXISTS)" = "false" ]; then \
        cp .env-template .env; \
    fi
	docker compose up -d --build

down:
	docker compose down
	
test: $(VENV_ACTIVATE) lint
	. $(VENV_ACTIVATE) && tox -e unit --skip-pkg-install
