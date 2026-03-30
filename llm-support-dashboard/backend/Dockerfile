# ---------------------------------------------------------------------------
# Dockerfile — Instructions for building a container image of the backend.
#
# WHAT IS A CONTAINER?
# Think of it as a lightweight virtual computer that contains your app
# and everything it needs to run. This means anyone can run your app
# without installing Python, PostgreSQL, etc. on their own machine.
# ---------------------------------------------------------------------------

# Start from an official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first (Docker caches this layer, making rebuilds faster)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Download the ML models during build so they're baked into the image
# (This makes container startup faster — no download needed at runtime)
RUN python -c "\
from transformers import pipeline; \
pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english'); \
pipeline('summarization', model='sshleifer/distilbart-cnn-12-6'); \
print('Models downloaded successfully!')"

# Tell Docker this container listens on port 8000
EXPOSE 8000

# The command to run when the container starts
# --host 0.0.0.0 makes the server accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
