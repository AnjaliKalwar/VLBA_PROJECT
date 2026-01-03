FROM ubuntu:24.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip3 install fastapi uvicorn mysql-connector-python

# Copy application code
COPY solution.py .

# Expose FastAPI port
EXPOSE 5000

# Run the application
CMD ["python3", "solution.py"]
