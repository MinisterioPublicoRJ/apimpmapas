FROM https://docker-registry-default.devcloud.mprj.mp.br/openshift/python:cadg

USER root

RUN pip install -U setuptools-scm

USER 1001
