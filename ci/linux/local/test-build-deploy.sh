#!/bin/bash
set -e

# set default values
BUILDING_IMAGE=lotti-building-image
RUNNING_IMAGE=lotti-running-image
WORK_FOLDER=/home/workfolder/
DEST_FOLDER=/home/artifacts/
SPEC_FOLDER="${DEST_FOLDER}"
HOST_DEST_FOLDER=$(realpath ~/artifacts/)
HOST_SPEC_FOLDER="${HOST_DEST_FOLDER}"


function check_essential_parameters()
{
    for PARAM in "$@"
    do
        if [ -z "${PARAM}" ]
        then
            echo "Error: mandatory parameter is missing"
            echo "provide at least SOURCE-FOLDER, SCRIPT, BUILDING-IMAGE, RUNNING-IMAGE, BUILDING-SCRIPT"
            exit 118
        fi
    done
}

function check_execution_result_in_container()
{
    if !(docker exec --workdir $1 $2 test -f $3)
    then
        echo "Error: file $3 does not exist"
        exit 119
    fi
    echo "file $3 exists"
    echo "Smoke test successful"
}

for ARGUMENT in "$@"

do

    KEY=$(echo "${ARGUMENT}" | cut -d= -f1)
    VALUE=$(echo "${ARGUMENT}" | cut -d= -f2)

    case "$KEY" in
            # folder where the project source code is stored
            SOURCE-FOLDER)      SOURCE_FOLDER=$(realpath "${VALUE}") ;;
            # main python executable file to compile
            SCRIPT)             SCRIPT="${VALUE}" ;;
            # the tag of the building docker image
            BUILDING-IMAGE)     BUILDING_IMAGE="${VALUE}" ;;
            # the tag of the running docker image
            RUNNING-IMAGE)      RUNNING_IMAGE="${VALUE}" ;;
            # script that does the compilation
            BUILDING-SCRIPT)    BUILDING_SCRIPT=$(realpath "${VALUE}") ;;
            HOST-DEST-FOLDER)   HOST_DEST_FOLDER=$(realpath "${VALUE}") ;;
            HOST-SPEC-FOLDER)   HOST_SPEC_FOLDER=$(realpath "${VALUE}") ;;
            # folder in container to store build artifacts (normally not given)
            DEST-FOLDER)        DEST_FOLDER="${VALUE}" ;;
            # folder in container to store work files during building (normally not given)
            WORK-FOLDER)        WORK_FOLDER="${VALUE}" ;;
            # folder in container to store spec file (normally not given)
            SPEC-FOLDER)        SPEC_FOLDER="${VALUE}" ;;
    esac

done

PARAM_ARRAY=("${SOURCE_FOLDER}" "${SCRIPT}" "${BUILDING_IMAGE}" "${RUNNING_IMAGE}" "${BUILDING_SCRIPT}")
check_essential_parameters "${PARAM_ARRAY[@]}"

BUILDING_CONTAINER=lotti-building-container
RUNNING_CONTAINER=lotti-running-container
# prepare container
set +e
docker container rm "${BUILDING_CONTAINER}" --force
set -e
echo Starting building container: "${BUILDING_CONTAINER}"
docker run -it -d --name "${BUILDING_CONTAINER}" "${BUILDING_IMAGE}" /bin/bash

SOURCE_IN_CONTAINER=/home/lotti-karotti-calculator/
echo Copy source code to "${BUILDING_CONTAINER}"...............................
docker cp "${SOURCE_FOLDER}"/config/ \
    "${BUILDING_CONTAINER}":"${SOURCE_IN_CONTAINER}"config/
docker cp "${SOURCE_FOLDER}"/logic/ \
    "${BUILDING_CONTAINER}":"${SOURCE_IN_CONTAINER}"logic/
docker cp "${SOURCE_FOLDER}"/tests/ \
    "${BUILDING_CONTAINER}":"${SOURCE_IN_CONTAINER}"tests/
docker cp "${SOURCE_FOLDER}"/game.py \
    "${BUILDING_CONTAINER}":"${SOURCE_IN_CONTAINER}"
docker cp "${SOURCE_FOLDER}"/requirements.txt \
    "${BUILDING_CONTAINER}":"${SOURCE_IN_CONTAINER}"
docker cp "${SOURCE_FOLDER}"/makefile \
    "${BUILDING_CONTAINER}":"${SOURCE_IN_CONTAINER}"
docker cp "${BUILDING_SCRIPT}" \
    "${BUILDING_CONTAINER}":"${SOURCE_IN_CONTAINER}"
docker exec --workdir "${SOURCE_IN_CONTAINER}" "${BUILDING_CONTAINER}" make

echo Running unit tests........................................................
docker exec \
    "${BUILDING_CONTAINER}" \
    pytest "${SOURCE_IN_CONTAINER}"tests/ > \
    "${HOST_DEST_FOLDER}"/unit-test-log.txt
VAR=$(<"${HOST_DEST_FOLDER}"/unit-test-log.txt)
# when finds nothing
VAR=$(echo $VAR | grep -o FAIL || true)
if [ -n "${VAR}" ]
then
  echo "One or more tests failed!"
  exit 125
fi
echo Unit test run successfuly!
echo report is saved on host under: "${HOST_DEST_FOLDER}"/unit-test-log.txt

#COMPILE PROGRAM
docker cp "${BUILDING_SCRIPT}" "${BUILDING_CONTAINER}":/home/cicd/
echo "${BUILDING_SCRIPT}" is copied to "${BUILDING_CONTAINER}":/home/cicd/

echo Starting compilation......................................................
docker exec \
    "${BUILDING_CONTAINER}" \
    /home/cicd/build.sh \
    SOURCE-FOLDER="${SOURCE_IN_CONTAINER}" \
    SCRIPT="${SCRIPT}" \
    WORK-FOLDER="${WORK_FOLDER}"/ \
    DEST-FOLDER="${DEST_FOLDER}"/ \
    SPEC-FOLDER="${SPEC_FOLDER}"/
echo Compilation completed!....................................................

docker cp "${BUILDING_CONTAINER}":"${DEST_FOLDER}"/ "${HOST_DEST_FOLDER}"/lotti/
echo compiled files are saved to host under: "${HOST_DEST_FOLDER}"/lotti/
docker stop "${BUILDING_CONTAINER}"
echo stop "${BUILDING_CONTAINER}"
echo Cleaning up folders in destination...
cp -R "${HOST_DEST_FOLDER}"/lotti/artifacts/. "${HOST_DEST_FOLDER}"/lotti/
rm -r "${HOST_DEST_FOLDER}"/lotti/artifacts/


set +e
echo removing container "${RUNNING_CONTAINER}"
docker container rm "${RUNNING_CONTAINER}" --force
set -e
echo starting up execution container: "${RUNNING_CONTAINER}"
docker run -it -d --name "${RUNNING_CONTAINER}" "${RUNNING_IMAGE}" /bin/bash
echo copy built artifacts to "${RUNNING_CONTAINER}"
docker cp "${HOST_DEST_FOLDER}"/lotti/ "${RUNNING_CONTAINER}":/home/

RESULT_FILE="result.txt"
EXEC_FOLDER=/home/lotti/

echo running smoke test for 2 players...
docker exec --workdir "${EXEC_FOLDER}" "${RUNNING_CONTAINER}" ./run_for_2.sh
check_execution_result_in_container \
    "${EXEC_FOLDER}" \
    "${RUNNING_CONTAINER}" \
    "${RESULT_FILE}"
docker exec --workdir "${EXEC_FOLDER}" \
    "${RUNNING_CONTAINER}" \
    rm "${RESULT_FILE}"

echo running smoke test for 3 players...
docker exec --workdir "${EXEC_FOLDER}" "${RUNNING_CONTAINER}" ./run_for_3.sh
check_execution_result_in_container \
    "${EXEC_FOLDER}" \
    "${RUNNING_CONTAINER}" \
    "${RESULT_FILE}"
docker exec --workdir "${EXEC_FOLDER}" \
    "${RUNNING_CONTAINER}" \
    rm "${RESULT_FILE}"

echo running smoke test for 4 players...
docker exec --workdir "${EXEC_FOLDER}" "${RUNNING_CONTAINER}" ./run_for_4.sh
check_execution_result_in_container \
    "${EXEC_FOLDER}" \
    "${RUNNING_CONTAINER}" \
    "${RESULT_FILE}"
docker exec --workdir "${EXEC_FOLDER}" \
    "${RUNNING_CONTAINER}" \
    rm "${RESULT_FILE}"

echo running smoke test for executable with parameters
docker exec --workdir "${EXEC_FOLDER}" "${RUNNING_CONTAINER}" ./game 5
check_execution_result_in_container \
    "${EXEC_FOLDER}" \
    "${RUNNING_CONTAINER}" \
    "${RESULT_FILE}"
docker exec --workdir "${EXEC_FOLDER}" \
    "${RUNNING_CONTAINER}" \
    rm "${RESULT_FILE}"

echo stopping "${RUNNING_CONTAINER}"
docker stop "${RUNNING_CONTAINER}"
echo COMPILATION AND TESTING FINISHED! PRODUCT IS READY TO DEPLOY!!!...........
