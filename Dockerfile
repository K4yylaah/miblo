FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

#recupere les packages
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

#recupere les fichier et dossiers dont on a besoins
COPY --chown=root:root ./Controllers /app/Controllers
COPY --chown=root:root ./models /app/models
COPY --chown=root:root ./routes /app/routes
COPY --chown=root:root ./testUnitaire /app/testUnitaire
COPY --chown=root:root ./main.py /app/main.py
COPY --chown=root:root ./database.py /app/database.py

#utilisation d'un user pour la sécurité
USER appuser

#Configuration du port
EXPOSE 8000

# Permettre d'acceder au site / sinon il tourne sur le localhost du container uniquement
# avec host et 0.0.0.0 on peux y acceder depuis le pc qui fait tourner le container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]