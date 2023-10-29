FROM python:3-alpine
WORKDIR /app

COPY requirements.txt \
    flaskapp.py \
    plq_sim.py \
    fret_calc.py \
    ri_calc.py \
    tmm_sim.py \
    init_script.sh \
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


RUN adduser -D nanocalc
ENV PATH="/home/nanocalc/.local/bin:${PATH}"
RUN chown -R nanocalc:nanocalc /app
USER nanocalc

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 443


USER root
COPY init_script.sh /app/init_script.sh
RUN chmod +x /app/init_script.sh
ENTRYPOINT ["/app/init_script.sh"]
