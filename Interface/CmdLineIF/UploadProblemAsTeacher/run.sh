#!/bin/bash

problems_base=$( readlink -f "/home/zhilts/PycharmProjects/TPy_project/problems_base" )
PYTHONPATH=..:../DataCustodian python3 main_driver.py $problems_base 1