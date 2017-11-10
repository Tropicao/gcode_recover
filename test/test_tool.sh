#!/bin/bash

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DATA_DIR=${TEST_DIR}/test_data
TOOL_DIR=${TEST_DIR}/..
TOOL_BIN="gcode_recover.py"

INPUT_FILAMENT="E8082.66163"
INPUT_FILE="pristine_gcode.gcode"
INPUT_FILE_PATH=${TEST_DATA_DIR}/${INPUT_FILE}

echo "Filament level : ${INPUT_FILAMENT}"
echo "Gcode file : ${INPUT_FILE_PATH}"
python ${TOOL_DIR}/${TOOL_BIN} ${INPUT_FILAMENT} ${INPUT_FILE_PATH}
