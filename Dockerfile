FROM openshift/python:cadg

USER root

RUN pip install -U setuptools-scm

USER 1001
