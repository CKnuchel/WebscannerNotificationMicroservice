FROM python:3.10-slim

WORKDIR /app

# Install curl to call the health check endpoint
RUN apt-get update && apt-get install -y curl

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
