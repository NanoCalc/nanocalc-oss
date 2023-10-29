#!/bin/bash

# Define color variables
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

# Get the Id of the current image
current_id=$(docker inspect --format='{{.Id}}' python:3-alpine)

# Pull the latest version of python:3-alpine from Docker Hub
docker pull python:3-alpine

# Get the Id of the latest image
latest_id=$(docker inspect --format='{{.Id}}' python:3-alpine)

# Compare the Ids
if [[ "$current_id" != "$latest_id" ]]; then
    # New version found
    echo -e "${GREEN}New version found. Would you like to update? (y/n)${NC}"
    read answer
    if [[ "$answer" == "y" ]]; then
        # Prepare for upgrade 
        ./update-visitors.sh
        docker stop nanocalc-container
        sleep 5
        docker rmi nanocalc-image

        # Create new, updated image
        cd ..
        git pull
        docker build -t nanocalc-image .

        # Cleanup old images
        docker image prune -f

        # Restart the service
        docker run --rm -d --name nanocalc-container -e DEBUG=False -p 443:443 -v nanocalc_ssl:/app/ssl nanocalc-image
    fi
else
    # No new version found
    echo -e "${YELLOW}No new version was found${NC}"
fi
