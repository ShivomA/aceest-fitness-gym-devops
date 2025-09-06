# Use Python image
FROM python:3.12-slim

# Install system packages for Tkinter + virtual display
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    xvfb \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files into container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default: run the app inside Xvfb (headless display)
CMD ["xvfb-run", "-a","pytest", "-v"]
