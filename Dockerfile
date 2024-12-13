# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY . .

# Set environment variables (adjust if needed)
ENV PYTHONUNBUFFERED=1

# Define the command to run the application
CMD ["python", "app.py"]