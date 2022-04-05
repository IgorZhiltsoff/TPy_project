#!/bin/bash

cd sample_tests
PYTHONPATH=.. python3 test_cxx.py
cd - >/dev/null
