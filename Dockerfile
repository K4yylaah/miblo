FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dossier de travail
WORKDIR /app

# Dépendances système
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Création d'un utilisateur non-root
RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

# Copie du code avec les bons droits
COPY --chown=appuser:appgroup ./Controllers .
COPY --chown=appuser:appgroup ./models .
COPY --chown=appuser:appgroup ./main.py .
COPY --chown=appuser:appgroup ./routes .
COPY --chown=appuser:appgroup ./testUnitaire .
COPY --chown=appuser:appgroup ./database.py .

# Droits d'accès
RUN chmod -R 755 /app

# On ne tourne plus en root
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]