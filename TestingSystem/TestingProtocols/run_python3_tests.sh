#!/bin/bash

cd sample_tests
PYTHONPATH=.. python3 test_python3.py
cd - >/dev/null
