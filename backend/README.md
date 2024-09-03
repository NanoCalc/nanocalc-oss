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
nanocalc-image
```

### Running in production mode:

```shell
docker run --rm -d --name nanocalc-container \
-e DEBUG=False -p 8080:8080 \
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


## Running with Python `venv` (for debugging):

Create a virtual environment, activate it and install dependencies:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Create local folders and run the main script:
```
./setup_local_env.sh

DEBUG=True PORT=8080 UPLOAD_FOLDER="nanocalc_uploads" python flaskapp.py
```
