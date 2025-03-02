## Nanocalc backend (Flask)

### Pre requisites:
- Python 3.x


You may take an individual look at the backend by running:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
This will create a virtual environment, activate it and install dependencies.

Next, create local folders (for processing user data) and run the main script in development mode:
```
./setup_local_env.sh
DEBUG=True PORT=8080 python flaskapp.py
```

This should run the development server at [localhost port 8080](http://localhost:8080).

You can also run unit and end to end tests by doing the following commands in the virtual environment:
```
pip install -r test_requirements.txt
coverage run -m unittest discover
```
