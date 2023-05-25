#!/bin/bash

cd sample_tests
PYTHONPATH=.. python3 test_abort.py
cd - >/dev/null
