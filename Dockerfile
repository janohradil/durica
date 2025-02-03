# Use official Python image
FROM python:alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

RUN pip install uv; uv init; uv pip install --system -r requirements.txt
# RUN uv init
# COPY pyproject.toml .
# RUN uv sync

# Copy the application code
COPY . .

# Expose the default FastAPI port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["fastapi", "dev"]
