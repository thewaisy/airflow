#!/bin/bash

AIRFLOW_VERSION='2.2.3'
PYTHON_VERSION='3.8'
USER='waisy'

echo "build docker image"
echo "Airflow version: ${AIRFLOW_VERSION}"
echo "Python version: ${PYTHON_VERSION}"


# build image
docker build \
    -t $USER/airflow:$AIRFLOW_VERSION-$PYTHON_VERSION \
    --build-arg AIRFLOW_IMAGE_NAME="apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}" \
    ./docker

# docker image push
# docker push $USER/airflow:$1-$2
