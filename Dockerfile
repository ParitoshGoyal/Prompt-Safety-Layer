# Use python image from dockerhub
FROM python:3.13

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install needed packages from requirements.txt
RUN pip install -r requirements.txt

# Make port 5000 available to world outside the container
EXPOSE 5000

# Run server.py when the container launches
CMD ["python", "server.py"]