#!/bin/bash
./manage.py collectstatic --noinput
# GUNICORN_CMD_ARGS = variável de configuração do Gunicorn
gunicorn mprj_api.wsgi:application --bind=0.0.0.0:8080 --log-file -
