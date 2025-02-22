# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements1.txt

# Run tests (this will fail the build if tests fail)
RUN pytest tests/

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to avoid python buffering
ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
CMD ["python", "restapi.py"]
