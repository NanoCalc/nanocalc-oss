# NanoCalc Open Source Repository
![NanoCalc Logo](https://github.com/NanoCalc/nanocalc-oss/assets/34662089/ccfab544-a9ab-4043-bf98-251da4179e90)

## Getting Started:

### Build the image:
```shell 
docker build -t nanocalc-image . --network=host
```
---
### Running in debug (local development) mode:
```shell
docker run --rm --name nanocalc-container -e DEBUG=True -p 8080:8080 nanocalc-image
```
---
### Running in production:

```shell
docker run --rm -d --name nanocalc-container -e DEBUG=False -p 8080:8080 nanocalc-image
```

## References:
[How to Create Efficient Python Docker Image](https://www.makeuseof.com/python-docker-image-create-efficient/)
