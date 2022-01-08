#!/bin/bash

echo "build docker image"
echo "Airflow version: ${1}"
echo "Python version: ${2}"

USER='waisy'

# build image
docker build \
    -t $USER/airflow:$1-$2 \
    --build-arg AIRFLOW_VERSION=$1 \
    ./docker

# docker image push
# docker push $USER/airflow:$1-$2
