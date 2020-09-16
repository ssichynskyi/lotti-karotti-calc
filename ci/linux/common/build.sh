#!/bin/bash
set -e
# set default values for some command line arguments
DEST_FOLDER=/home/dist/
WORK_FOLDER=/home/build/
SPEC_FOLDER="${DEST_FOLDER}"

for ARGUMENT in "$@"

do

    KEY=$(echo "${ARGUMENT}" | cut -d= -f1)
    VALUE=$(echo "${ARGUMENT}" | cut -d= -f2)

    case "$KEY" in
            # folder on host with the source code for build
            SOURCE-FOLDER)   SOURCE_FOLDER=$(realpath "${VALUE}")/ ;;
            # main script (python file) in the SOURCE-FOLDER
            SCRIPT)          SCRIPT="${VALUE}" ;;
            # folder in container to store build files
            DEST-FOLDER)     DEST_FOLDER=$(realpath "${VALUE}")/ ;;
            # folder in container to store temp/working build files
            WORK-FOLDER)     WORK_FOLDER="${VALUE}" ;;
            # folder in container to store spec file
            SPEC-FOLDER)     SPEC_FOLDER=$(realpath "${VALUE}") ;;
    esac

done

pyinstaller \
    --noconfirm \
    --onefile \
    --nowindow \
    --clean \
    --workpath "${WORK_FOLDER}" \
    --distpath "${DEST_FOLDER}" \
    --specpath "${SPEC_FOLDER}" \
    "${SOURCE_FOLDER}""${SCRIPT}"

cp "${SOURCE_FOLDER}"/config "${DEST_FOLDER}" -r -f

echo "create script files for fast run"
for i in {2..4}

do
# empty file content
> "${DEST_FOLDER}"run_for_"${i}".sh
cat << 'EOF' >> "${DEST_FOLDER}"run_for_"${i}".sh
#!/bin/bash
$(dirname $(realpath "$0"))\
EOF

cat << EOF >> "${DEST_FOLDER}"run_for_"${i}".sh
/game ${i}

EOF
chmod +x "${DEST_FOLDER}"run_for_"${i}".sh
done

echo "Compilation completed successfully!"
# this is just a save for the future - comment block
: << COMMENT
COMMENT
