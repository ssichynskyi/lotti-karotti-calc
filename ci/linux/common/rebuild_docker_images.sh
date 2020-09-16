#!/bin/bash
set -e
# set default values for some command line arguments

for ARGUMENT in "$@"

do

    KEY=$(echo "${ARGUMENT}" | cut -d= -f1)
    VALUE=$(echo "${ARGUMENT}" | cut -d= -f2)

    case "$KEY" in
            # path to docker file for building image
            BUILDING-DOCKER-FILE)         BUILDING_DOCKER_FILE="${VALUE}" ;;
            # path to docker file for running image
            RUNNING-DOCKER-FILE)          RUNNING_DOCKER_FILE="${VALUE}" ;;
    esac

done

BUILDING_FOLDER=$(realpath $(dirname "${BUILDING_DOCKER_FILE}"))/
RUNNING_FOLDER=$(realpath $(dirname "${RUNNING_DOCKER_FILE}"))/
# remove old images
set +e
docker image rm lotti-building-image --force
docker image rm lotti-running-image --force
set -e
# build new images
docker build -t lotti-building-image -f "${BUILDING_DOCKER_FILE}" "${BUILDING_FOLDER}"
docker build -t lotti-running-image -f "${RUNNING_DOCKER_FILE}" "${RUNNING_FOLDER}"
