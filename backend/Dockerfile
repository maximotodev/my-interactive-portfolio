# backend/Dockerfile

# 1. Start with a stable Python base image
FROM python:3.12-slim

# 2. Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install system dependencies (like build tools)
# This is often needed for packages with C-extensions.
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential

# 5. Copy the requirements file and install Python packages
# This step is cached, so it only re-runs if requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your backend application code into the container
COPY . .

# 7. The port Hugging Face Spaces expects the app to run on
EXPOSE 7860

# 8. The command to run when the container starts.
# We bind Gunicorn to port 7860 as required by Hugging Face.
CMD ["python", "-m", "gunicorn", "--config", "gunicorn.conf.py", "--bind", "0.0.0.0:7860", "portfolio_project.wsgi"]