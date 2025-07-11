# Dockerfile (in the project root)

# 1. Start with a stable Python base image
FROM python:3.12-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set the working directory
WORKDIR /app

# 4. Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential

# --- THIS IS THE CRITICAL CHANGE ---
# 5. Copy ONLY the requirements file from the backend directory first
COPY backend/requirements.txt .

# 6. Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy the entire backend directory into the container
COPY backend/ .

# 8. The port Hugging Face Spaces expects the app to run on
EXPOSE 7860

# 9. The command to run when the container starts.
#    Note that the paths inside the container are now flat.
CMD ["python", "-m", "gunicorn", "--config", "gunicorn.conf.py", "--bind", "0.0.0.0:7860", "portfolio_project.wsgi"]