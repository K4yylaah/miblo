FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \ build-essential \&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY --chown=root:root --chmod=755 src ./Controllers
COPY --chown=root:root --chmod=755 src ./models
COPY --chown=root:root --chmod=755 src ./routes
COPY --chown=root:root --chmod=755 src ./testUnitaire
COPY --chown=root:root --chmod=755 src ./database.py
COPY --chown=root:root --chmod=755 src ./main.py


EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
