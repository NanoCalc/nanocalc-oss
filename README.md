# NanoCalc Open Source Repository

## Getting started:

### Build the image:
```shell 
docker build -t nanocalc-image . --network=host
```

### Running in debug (local development) mode:
```shell
docker run --rm --name nanocalc-container \
-e DEBUG=True -p 8080:8080 \
-v $(pwd)/GeoIP.dat:/app/GeoIP.dat \
-v $(pwd)/visitors.db:/app/visitors.db \
nanocalc-image
```

### Running in production mode:

```shell
docker run --rm -d --name nanocalc-container \
-e DEBUG=False -p 8080:8080 \
-v $(pwd)/GeoIP.dat:/app/GeoIP.dat \
-v $(pwd)/visitors.db:/app/visitors.db \
nanocalc-image
```

## Running tests:

### If non existent, create a Python virtual environment and activate it: 
```shell
python3 -m venv env
source env/bin/activate
```

### Install test dependencies:
```shell
pip install -r test_requirements.txt
```

### Run the test suite:
```shell
coverage run -m unittest discover
```
