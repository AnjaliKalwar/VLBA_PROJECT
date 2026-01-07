FROM python:3.12-slim

WORKDIR /app

# Install dependencies (no apt, no venv)
RUN pip install --no-cache-dir fastapi uvicorn mysql-connector-python

# Copy application
COPY solution.py .

# Match the port used inside solution.py
EXPOSE 5000

# Run solution.py directly (uvicorn starts inside it)
CMD ["python", "solution.py"]
