FROM python:3.12-alpine3.20 

ENV PATH="/home/nanocalc/.local/bin:${PATH}"

RUN adduser -D nanocalc
USER nanocalc
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY flaskapp.py \
    plqsim_core.py \
    plqsim_facade.py \
    fretcalc_core.py \
    ricalc_core.py \
    tmmsim_core.py \
    tmmsim_auxiliary_functions.py \
    tmmsim_computation_functions.py \
    config.py \
    helper_functions.py \
    apps_definitions.py \
    /app/

    
RUN mkdir -p /app/upload/fretcalc/result \
    /app/upload/ricalc/result \
    /app/upload/plqsim/result \
    /app/upload/tmmsim/result \
    /app/backend/logs


EXPOSE 8080
CMD ["python", "flaskapp.py"]
