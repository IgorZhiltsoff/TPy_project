#!/bin/bash

mount_point=$( realpath "$( dirname "$(realpath $0)" )/../../..")
problems_base="$mount_point/problems_base"
# shellcheck disable=SC2046
PYTHONPATH=..:../../../TestingSystem/TestingProtocols python3 main_driver.py "$problems_base" "$( realpath "$mount_point/.." )"