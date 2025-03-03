# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application files
COPY . /app

# Set PYTHONPATH to the app directory
ENV PYTHONPATH=/app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to avoid python buffering
ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
CMD ["python", "restapi.py"]
