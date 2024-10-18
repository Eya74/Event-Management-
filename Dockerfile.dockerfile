# Use the official Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential curl \
    && apt-get clean

# Install Node.js (LTS version 16.x)
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest

# Create and set the working directory
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app/
RUN python -m venv venv \
    && . venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the required ports (5000 for Flask and 3000 for Node.js if needed)
EXPOSE 5000
EXPOSE 3000

# Specify the default command to run your app
CMD ["/bin/bash", "-c", "source venv/bin/activate && flask run --host=0.0.0.0"]
