#!/bin/bash

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DATA_DIR=${TEST_DIR}/test_data
TOOL_DIR=${TEST_DIR}/..
python ${TOOL_DIR}/gcode_recover.py E1857.38 ${TEST_DATA_DIR}/pristine_gcode.gcode
