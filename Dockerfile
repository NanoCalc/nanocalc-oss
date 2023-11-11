FROM python:3-alpine
EXPOSE 8080
ENV PATH="/home/nanocalc/.local/bin:${PATH}"
WORKDIR /app

COPY requirements.txt /app/
RUN adduser -D nanocalc
USER nanocalc
RUN pip install --no-cache-dir -r requirements.txt
USER root

COPY flaskapp.py \
    plq_sim.py \
    fret_calc.py \
    ri_calc.py \
    tmm_sim.py \
    visitors.txt \
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


RUN chown -R nanocalc:nanocalc /app

USER nanocalc
CMD ["python", "flaskapp.py"]
