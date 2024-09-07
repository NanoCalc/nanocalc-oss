FROM python:3-alpine

ENV PATH="/home/nanocalc/.local/bin:${PATH}"

RUN adduser -D nanocalc
USER nanocalc
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY flaskapp.py \
    plq_sim.py \
    fret_calc.py \
    ri_calc.py \
    tmm_sim.py \
    config.py \
    helper_functions.py \
    apps_definitions.py \
    /app/

    
RUN mkdir -p /app/upload/fretcalc/result \
    /app/upload/ricalc/result \
    /app/upload/plqsim/result \
    /app/upload/tmmsim/result


EXPOSE 8080
CMD ["python", "flaskapp.py"]
