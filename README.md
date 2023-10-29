# NanoCalc Open Source Repository
![NanoCalc Logo](https://github.com/NanoCalc/nanocalc-oss/assets/34662089/ccfab544-a9ab-4043-bf98-251da4179e90)

## Getting Started
### Running in debug (local development) mode:

#### Build the image:
```shell 
docker build -t nanocalc-image .
```

#### Run the container:
```shell
docker run --rm --name nanocalc-container -e DEBUG=True -p 80:80 nanocalc-image
```
---
### Running in production:

#### Build the image:
```shell 
docker build -t nanocalc-image .
```

#### Create a volume for SSL certificates:
```shell
docker volume create nanocalc_ssl
```

#### Run the container: 
```shell
docker run --rm -d --name nanocalc-container -e DEBUG=False -p 443:443 -v nanocalc_ssl:/app/ssl nanocalc-image
```

---
### References:
[How to Create Efficient Python Docker Image](https://www.makeuseof.com/python-docker-image-create-efficient/)
