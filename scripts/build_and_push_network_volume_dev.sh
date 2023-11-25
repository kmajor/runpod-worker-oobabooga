#!/bin/bash
set -e

# Function to check if the user is logged in to Docker Hub
check_docker_login() {
    # Try to get the login status by searching for the username in `docker info` output
    if docker info | grep -q "Username:"; then
        echo "You are already logged in to Docker Hub."
    else
        echo "You are not logged in to Docker Hub."
        echo "Please login to continue."
        docker login
    fi
}

# Check Docker login status and authenticate if necessary
check_docker_login

# Define image name and tag
IMAGE_NAME="runpod-oobabooga-network-volume"
TAG="dev"
DOCKERHUB_USERNAME="majorbros"
FULL_IMAGE_NAME="$DOCKERHUB_USERNAME/$IMAGE_NAME:$TAG"

# Build the Docker image
docker build -t $FULL_IMAGE_NAME -f ./Dockerfile.Network_Volume .

# Push the Docker image to Docker Hub
docker push $FULL_IMAGE_NAME

echo "Docker image $FULL_IMAGE_NAME has been built and pushed to Docker Hub."

