#!/bin/bash

problems_base=$( readlink -f "/home/zhilts/PycharmProjects/TPy_project/problems_base" )
PYTHONPATH=..:../../../TestingSystem/TestingProtocols python3 main_driver.py "$problems_base"