# NanoCalc Open Source Repository
![NanoCalc Logo](https://github.com/NanoCalc/nanocalc-oss/assets/34662089/ccfab544-a9ab-4043-bf98-251da4179e90)

## Standard usage (Docker container):

### Build the image:
```shell 
docker build -t nanocalc-image . --network=host
```

### Running in debug (local development) mode:
```shell
docker run --rm --name nanocalc-container \
-e DEBUG=True -p 8080:8080 \
-v GeoIP.dat:/app/GeoIP.dat \
-v visitors.db:/app/visitors.db \
nanocalc-image
```

### Running in production:

```shell
docker run --rm -d --name nanocalc-container \
-e DEBUG=False -p 8080:8080 \
-v $(pwd)/GeoIP.dat:/app/GeoIP.dat \
-v $(pwd)/visitors.db:/app/visitors.db \
nanocalc-image
```

### Run tests:
```shell
coverage run -m unittest discover
```

## Direct usage (with Python virtual environment):

### First, create a virtual environment and activate it:
```shell
python3 -m venv env
source venv/bin/activate
```

### Install project and test dependencies:
```shell
pip install -r requirements.txt
pip install -r test_requirements.txt
```

### Setup local environment:

```shell
./setup_local_env.sh
```

### Start the server:
```shell
DEBUG=True PORT=8080 UPLOAD_FOLDER="app/upload" python flaskapp.py
```

### Run tests:
```shell
coverage run -m unittest discover
```


## References:
[How to Create Efficient Python Docker Image](https://www.makeuseof.com/python-docker-image-create-efficient/)
