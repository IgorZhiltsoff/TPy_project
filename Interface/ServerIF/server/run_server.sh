#!/bin/bash

PYTHONPATH=../../CmdLineIF/:../../CmdLineIF/UploadSubmissionAsStudent:../../../TestingSystem/TestingProtocols/ python3 server.py "$1" "$2"