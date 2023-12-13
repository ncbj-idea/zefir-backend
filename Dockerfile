FROM docker.nexus.services.idea.edu.pl/library/python:3.11

WORKDIR /code

COPY ./requirements.txt /requirements.txt
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y gdal-bin libgdal-dev --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade -r /requirements.txt \
    --index-url https://nexus.services.idea.edu.pl/repository/pypi-all/simple

COPY ./zefir_api /code/zefir_api
COPY ./simple-data-case /code/simple-data-case

CMD ["sh", "-c", "python -m gunicorn -c /code/zefir_api/api/gunicorn_config.py zefir_api.api.main:app"]
