# Stage 1: Build stage
FROM python:3.12 AS builder

WORKDIR /app

# Install dependencies into a virtual environment to make copying easy
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy the pre-compiled Python packages from the builder stage
COPY --from=builder /opt/venv /opt/venv
COPY . .

# Ensure the virtual environment is used
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000
CMD ["python", "main.py"]