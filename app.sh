#!/bin/bash
if [ -z "$WORKER" ]
then
    # GUNICORN_CMD_ARGS = variável de configuração do Gunicorn
    ./manage.py collectstatic --noinput
    NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn mprj_api.wsgi:application --workers=24 --threads = 2 --bind=0.0.0.0:8080 --log-file -
else
    celery -A lupa.tasks worker -l info --pool=solo
fi
