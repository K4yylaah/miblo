FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

# Code en lecture seule
COPY --chown=root:root --chmod=755 ./Controllers ./Controllers
COPY --chown=root:root --chmod=755 ./models ./models
COPY --chown=root:root --chmod=755 ./routes ./routes
COPY --chown=root:root --chmod=755 ./testUnitaire ./testUnitaire
COPY --chown=root:root --chmod=644 ./main.py .
COPY --chown=root:root --chmod=644 ./database.py .

# Dossier writable pour SQLite
RUN mkdir /app/data \
    && chown appuser:appgroup /app/data \
    && chmod 700 /app/data

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
