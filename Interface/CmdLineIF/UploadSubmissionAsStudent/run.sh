#!/bin/bash

# shellcheck disable=SC2046
# shellcheck disable=SC2164
cd $( dirname "$0" )

mount_point=$( realpath "$( dirname "$(realpath "$0")" )/../../..")
problems_base="$mount_point/problems_base"
# shellcheck disable=SC2046
PYTHONPATH=..:../../../TestingSystem/TestingProtocols python3 main_driver.py "$problems_base" "$1" "$( realpath "$mount_point/.." )"