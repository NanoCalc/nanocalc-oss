#!/bin/sh 

docker cp nanocalc-container:/app/visitors.txt ../
cp ../visitors.txt ../../
