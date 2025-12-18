FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \ && apt-get install -y --no-install-recommends ca-certificates \ && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \ && pip install --no-cache-dir -r requirements.txt && addgroup --system appgroup \ && adduser --system --ingroup appgroup appuser

# Code en lecture seule
COPY --chown=root:root ./Controllers /app/Controllers
COPY --chown=root:root ./models /app/models
COPY --chown=root:root ./routes /app/routes
COPY --chown=root:root ./testUnitaire /app/testUnitaire
COPY --chown=root:root ./main.py /app/main.py
COPY --chown=root:root ./database.py /app/database.py

# Permissions lecture seule pour le code
RUN chmod -R 555 /app \ && mkdir -p /app/data \ && chown -R appuser:appgroup /app/data \ && chmod 700 /app/data

USER appuser

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]