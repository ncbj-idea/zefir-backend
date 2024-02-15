ARG DOCKER_IMAGE=python:3.11
# hadolint ignore=DL3006
FROM $DOCKER_IMAGE as builder
ARG PIP_INDEX=https://pypi.org/simple
ENV PIP_INDEX_URL=$PIP_INDEX

COPY ./zefir_api ${HOME}/wspace/zefir_api
COPY ./pyproject.toml ${HOME}/wspace/

WORKDIR ${HOME}/wspace/

RUN pip install build==1.0.3 --no-cache-dir && python -m build --wheel

# hadolint ignore=DL3006
FROM $DOCKER_IMAGE
ARG PIP_INDEX=https://pypi.org/simple
ENV PIP_INDEX_URL=$PIP_INDEX
COPY --from=builder ${HOME}/wspace/dist/*.whl /code/
COPY ./simple-data-case /code/simple-data-case
COPY ./zefir_api/api/gunicorn_config.py /code/zefir_api/api/gunicorn_config.py
WORKDIR /code
# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y gdal-bin libgdal-dev --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir /code/*.whl

CMD ["sh", "-c", "python -m gunicorn -c /code/zefir_api/api/gunicorn_config.py zefir_api.api.main:app"]
