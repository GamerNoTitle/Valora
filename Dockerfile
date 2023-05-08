# Use Python 3.10 as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the application code to the working directory inside the container
COPY . /app

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV REDIS_URL $REDIS_URL
ENV REDIS_HOST $REDIS_HOST
ENV REDIS_PASSWORD $REDIS_PASSWORD
ENV REDIS_SSL $REDIS_SSL
ENV REDIS_PORT $REDIS_PORT
ENV PORT $PORT
# filesystem | redis
ENV SESSION_TYPE $SESSION_TYPE

# Expose the application port
EXPOSE $PORT

# Start the application
CMD ["python3","app.py"]
