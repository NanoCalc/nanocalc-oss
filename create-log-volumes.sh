#!/bin/sh
set -ex

mkdir -p ./logs/nginx
sudo chown -R 101:101 ./logs/nginx

mkdir -p ./logs/backend
sudo chown -R 1000:1000 ./logs/backend