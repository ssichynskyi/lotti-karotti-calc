#!/bin/bash

# set default values for some command line arguments
BUILDING_DOCKER_FILE=$(realpath docker-files/for-building-local)
RUNNING_DOCKER_FILE=$(realpath ../common/docker-files/for-running)

# set default values
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

../common/rebuild_docker_images.sh BUILDING-DOCKER-FILE="${BUILDING_DOCKER_FILE}" RUNNING-DOCKER-FILE="${RUNNING_DOCKER_FILE}"
