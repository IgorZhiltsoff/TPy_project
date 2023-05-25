#!/bin/bash

PYTHONPATH=../../CmdLineIF/:../../CmdLineIF/UploadSubmissionAsStudent:../../../TestingSystem/TestingProtocols/:/usr/lib/python310.zip:/usr/lib/python3.10:/usr/lib/python3.10/lib-dynload:/home/zhilts/.local/lib/python3.10/site-packages:/usr/lib/python3.10/site-packages:.. python3 server.py "$1" "$2"
