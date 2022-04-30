#!/bin/bash

# shellcheck disable=SC2164
cd sample_tests
PYTHONPATH=.. python -m unittest discover .
