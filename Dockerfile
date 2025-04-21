# Use an official Python runtime
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for Tkinter, OpenCV, and Docker
RUN apt-get update && \
    apt-get install -y \
    python3-tk \
    libgl1-mesa-glx \
    libglib2.0-0 \
    docker.io && \
    rm -rf /var/lib/apt/lists/*

# (Removed: usermod -aG docker jenkins)

# Set work directory
WORKDIR /app

# Copy everything into the container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --timeout=300 -r requirements.txt

# Expose the port Flask runs on (if needed)
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
