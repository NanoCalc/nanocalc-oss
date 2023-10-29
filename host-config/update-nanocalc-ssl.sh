#!/bin/bash
# Place this in /etc/letsencrypt/renewal-hooks/deploy/

DOMAIN="nanocalc.org"
VOLUME_NAME="nanocalc_ssl"

# Check if the renewal was for our specific domain
if [[ "$RENEWED_DOMAINS" == *"$DOMAIN"* ]]; then
    # Copy the actual certificate files (not symbolic links) to the Docker volume
    docker run --rm \
               -v $VOLUME_NAME:/to \
               -v /etc/letsencrypt/archive/$DOMAIN:/from \
               alpine sh -c "cp /from/fullchain1.pem /to/fullchain.pem && cp /from/privkey1.pem /to/privkey.pem"
fi

docker restart nanocalc-container
