#!/bin/bash
if [ -z "$WORKER" ]
then
    # GUNICORN_CMD_ARGS = variável de configuração do Gunicorn
    ./manage.py collectstatic --noinput
    gunicorn mprj_api.wsgi:application --bind=0.0.0.0:8080 --log-file -
else
    celery -A lupa.tasks worker -l info --pool=solo
fi
