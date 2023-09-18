# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD /src /app
ADD /src/planning_permission/requirements.txt /app

# Install any needed packages specified in requirements.txt 
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run chainlit when the container launches
CMD ["python", "-m", "chainlit", "run", "planning_permission/app_main_stream.py", "--port", "80"]
