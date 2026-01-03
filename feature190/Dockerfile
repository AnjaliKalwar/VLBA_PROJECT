FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Install Python + venv
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create virtual environment
RUN python3 -m venv /opt/venv

# Activate venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies INSIDE venv (PEP 668 compliant)
RUN pip install fastapi uvicorn mysql-connector-python

# Copy application
COPY solution.py .

EXPOSE 5000

# Run application
CMD ["python", "solution.py"]
