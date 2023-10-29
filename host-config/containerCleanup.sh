#!/bin/sh 

docker stop nanocalc-container 
sleep 5
docker rmi nanocalc-image
