FROM python:3.13-bookworm as builder



RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY ./pyproject.toml .

RUN uv sync

# ---------------------
# Final stage
FROM python:3.13-slim-bookworm AS final

WORKDIR /app
COPY csv init-db PKDD app.py create_db_app wait-for-it.sh ./project/
COPY --from=builder /app/.venv venv

ENV PATH="/app/.venv/bin:$PATH"

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

ENV FLASK_ENV=production

# CMD ["python", "create_db_app.py"]