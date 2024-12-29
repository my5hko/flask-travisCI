FROM python:3.12
# 3.12 is the latest version of python
WORKDIR /app 
# Set the working directory to /app
COPY . /app 
# Copy the current directory contents into the container at /app
RUN pip install -r requirements.txt 
# Install any needed packages specified in requirements.txt
RUN flask db upgrade 
# Run the database migrations
EXPOSE 5000 
# Make port 5000 available to the world outside this container
CMD gunicorn -w 4 --bind 0.0.0.0:5000 'app:create_app()' --reload
# Run app using gunicorn with 4 workers, entry point 'app:create_app()' to run create_app() function from app folder and reload the app when code changes, 
#bind to 0.0.0.0:$PORT to make it available to the world outside the container


