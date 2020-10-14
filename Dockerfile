FROM openshift/python:cadg

USER root

pip install -U setuptools-scm

USER 1001
