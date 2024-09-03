FROM python:3-alpine

LABEL maintainer="OmarMesqq" 
LABEL contact="omarmsqt@gmail.com" 
LABEL description="nanocalc.org Flask application"
LABEL version="1.0"

EXPOSE 8080
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

    
RUN mkdir -p /app/upload/fret/emission_files \
    /app/upload/fretcalc/extinction_coefficient_files \
    /app/upload/fretcalc/index_files \
    /app/upload/fretcalc/refractive_index_files \
    /app/upload/fretcalc/result \
    /app/upload/ricalc/index_files \
    /app/upload/ricalc/abs_coefficient_files \
    /app/upload/ricalc/k_files \
    /app/upload/ricalc/result \
    /app/upload/plqsim/input_files \
    /app/upload/plqsim/result \
    /app/upload/tmmsim/input_files \ 
    /app/upload/tmmsim/result


CMD ["python", "flaskapp.py"]
