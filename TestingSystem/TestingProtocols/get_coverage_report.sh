#!/bin/bash

# shellcheck disable=SC2164
cd sample_tests

sudo PYTHONPATH=:/usr/lib/python310.zip:/usr/lib/python3.10:/usr/lib/python3.10/lib-dynload:/home/zhilts/.local/lib/python3.10/site-packages:/usr/lib/python3.10/site-packages:.. coverage run -m --omit=*test_*.py unittest discover

coverage report -m
coverage html
