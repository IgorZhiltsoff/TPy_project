#!/bin/bash

dir_with_this_script="$( dirname "$(realpath "$0")" )"
cd $dir_with_this_script

mount_point=$( realpath "$dir_with_this_script/../../..")
problems_base="$mount_point/problems_base"

PYTHONPATH=..:../DataCustodian python3 main_driver.py "$problems_base" 0 "1.0.0"
