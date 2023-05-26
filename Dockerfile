# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Make the wait-for-it.sh script executable
RUN chmod +x /app/wait-for-it.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Use the wait-for-it.sh script to wait for the db service to be available, then run main.py
CMD ["/app/wait-for-it.sh", "db:5432", "-t", "120", "--", "python", "./main.py"]
