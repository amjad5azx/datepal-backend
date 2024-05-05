echo "FROM python:3" > Dockerfile
echo "RUN pip3 install django daphne channels pillow numpy tensorflow pymongo django-cors-headers channels_redis" >> Dockerfile
echo "COPY . ." >> Dockerfile
echo "RUN python manage.py migrate" >> Dockerfile
echo 'CMD ["daphne", "-b", "0.0.0.0", "-p", "8001", "fyp_backend.asgi:application"]' >> Dockerfile

# Build the Docker image
sudo docker build . -t fyp_backend

# Run the Docker container
container_id=$(sudo docker run -p 8001:8001 fyp_backend)

# Display the Container ID
echo "Docker container ID: $container_id"
