#!/bin/bash

rm -r /tmp/nsp
cp -r ../../../../nonsystem_problem /tmp/nsp

cd ..
./run.sh <sample_test/input
