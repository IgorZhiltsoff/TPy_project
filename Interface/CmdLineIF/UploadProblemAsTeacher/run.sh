#!/bin/bash

mount_point=$( realpath "$( dirname "$(realpath "$0")" )/../../..")
problems_base="$mount_point/problems_base"

PYTHONPATH=..:../DataCustodian python3 main_driver.py "$problems_base" 1 "1.0.0"