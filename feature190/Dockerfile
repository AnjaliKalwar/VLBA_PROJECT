FROM ubuntu:24.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# 🔹 Install Python dependencies directly (NO requirements.txt)
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    mysql-connector-python

# Copy application code
COPY . .

# Expose app port
EXPOSE 5000

# Optional: wait for DBs before starting
CMD ["sh", "-c", "nc -z db1 3306 && nc -z db2 3306 && python solution.py"]
