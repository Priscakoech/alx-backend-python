# 1. Use Python 3.10 as the base image (like starting with a ready-made OS that already has Python installed)
FROM python:3.10

# 2. Environment settings (make Python run better inside Docker)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container (like saying "cd /app")
WORKDIR /app

# 4. Copy your requirements.txt into the container and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your Django project code into the container
COPY . /app/

# 6. Tell Docker which port Django will use
EXPOSE 8000

# 7. Command to start Django when the container runs
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#docker run -p 8000:8000 messaging_app_image
