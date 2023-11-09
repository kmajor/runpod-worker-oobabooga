#!/bin/bash

# Check if the network exists
network_exists=$(docker network ls --filter name=^babylon_dev_network$ --format="{{ .Name }}")

# Create the network only if it doesn't exist
if [ -z "$network_exists" ]; then
  echo "Creating network babylon_dev_network"
  docker network create babylon_dev_network
else
  echo "Network babylon_dev_network already exists"
fi

# Build the Docker image using the development Docker Compose file
docker build . -f Dockerfile.StandaloneCpu -t runpod-oobabooga-cpu

docker run --network babylon_dev_network -v /Users/weekev/work/runpod/runpod-worker-oobabooga/rp_handler.py:/rp_handler.py -p 5001:5000 runpod-oobabooga-cpu
