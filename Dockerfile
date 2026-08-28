# --- Build stage: install dependencies into a clean layer ---
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# --- Final stage: minimal runtime image ---
FROM python:3.12-slim

# Run as a non-root user (security best practice)
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /app

# Bring in installed packages from the builder stage
COPY --from=builder /root/.local /home/appuser/.local
COPY app.py db.py models.py .
COPY static ./static

# Directory for the SQLite file (mounted as a volume for persistence).
# Owned by appuser so the non-root process can write to it.
RUN mkdir -p /app/data && chown -R appuser:appuser /app

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PORT=5000

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--preload", "app:app"]