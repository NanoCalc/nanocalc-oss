#!/bin/sh 

./update-visitors.sh
docker stop nanocalc-container 
sleep 5
docker rmi nanocalc-image
