# NanoCalc Open Source Repository
![NanoCalc Logo](https://github.com/NanoCalc/nanocalc-oss/assets/34662089/ccfab544-a9ab-4043-bf98-251da4179e90)

## Standard usage (Docker container):

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

--- 

## Direct usage (with Python virtual environment):

### First, create a virtual environment and activate it:
```shell
python3 -m venv venv
source venv/bin/activate
```

### Install project and test dependencies:
```shell
pip install -r requirements.txt
pip install -r test/requirements.txt
```

### Setup mocks and local environment:

```shell
./setup_local_env.sh
./setup_mocks.sh
```

### Start the server:
```shell
DEBUG=True PORT=8080 UPLOAD_FOLDER="app/upload" python flaskapp.py
```

### Run tests:
```shell
python test/nanocalc_e2e_test.py
```


## References:
[How to Create Efficient Python Docker Image](https://www.makeuseof.com/python-docker-image-create-efficient/)
