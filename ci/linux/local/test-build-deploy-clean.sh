#!/bin/bash
set -e

# set default values for some command line arguments
BUILDING_DOCKER_FILE=$(realpath docker-files/for-building-local)
RUNNING_DOCKER_FILE=$(realpath ../common/docker-files/for-running)
BUILDING_IMAGE=lotti-building-image
RUNNING_IMAGE=lotti-running-image
BUILDING_SCRIPT=BUILDING_FOLDER=$(realpath ../common/build.sh)

for ARGUMENT in "$@"

do

    KEY=$(echo "${ARGUMENT}" | cut -d= -f1)
    VALUE=$(echo "${ARGUMENT}" | cut -d= -f2)

    case "$KEY" in
            # docker file path for building image
            BUILDING-DOCKER-FILE)   BUILDING_DOCKER_FILE="${VALUE}" ;;
            # docker file path for running image
            RUNNING-DOCKER-FILE)    RUNNING_DOCKER_FILE="${VALUE}" ;;
            # folder where the project source code is stored
            SOURCE-FOLDER)          SOURCE_FOLDER="${VALUE}" ;;
            # main python executable file to compile
            SCRIPT)                 SCRIPT="${VALUE}" ;;
            # the tag of the building docker image
            BUILDING-IMAGE)         BUILDING_IMAGE="${VALUE}" ;;
            # the tag of the running docker image
            RUNNING-IMAGE)          RUNNING_IMAGE="${VALUE}" ;;
            # script that does the compilation
            BUILDING-SCRIPT)        BUILDING_SCRIPT="${VALUE}" ;;

    esac

done

##########REBUILD DOCKER IMAGES#############
./rebuild_docker_images_for_local.sh BUILDING-DOCKER-FILE="${BUILDING_DOCKER_FILE}" RUNNING-DOCKER-FILE="${RUNNING_DOCKER_FILE}"
############TEST-BUILD-DEPLOY###############
./test-build-deploy.sh SOURCE-FOLDER="${SOURCE_FOLDER}" SCRIPT=game.py BUILDING-IMAGE="${BUILDING_IMAGE}" RUNNING-IMAGE="${RUNNING_IMAGE}" BUILDING-SCRIPT="${BUILDING_SCRIPT}"
