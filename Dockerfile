FROM python:3-alpine
EXPOSE 8080
ENV PATH="/home/nanocalc/.local/bin:${PATH}"

RUN adduser -D nanocalc
USER nanocalc
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY flaskapp.py \
    upload_error.py \
    plq_sim.py \
    fret_calc.py \
    ri_calc.py \
    tmm_sim.py \
    config.py \
    visitor.py \
    helper_functions.py \
    /app/

COPY static /app/static
COPY templates /app/templates

RUN mkdir -p /app/upload/fret/emission_files \
    /app/upload/fret/extinction_coefficient_files \
    /app/upload/fret/index_files \
    /app/upload/fret/refractive_index_files \
    /app/upload/fret/result \
    /app/upload/ri/index_files \
    /app/upload/ri/abs_coefficient_files \
    /app/upload/ri/k_files \
    /app/upload/ri/result \
    /app/upload/plqsim/input_files \
    /app/upload/plqsim/result \
    /app/upload/tmmsim/input_files \ 
    /app/upload/tmmsim/result


CMD ["python", "flaskapp.py"]
