#!/bin/bash

## Copyright (c) 2020 mangalbhaskar.
# __author__='mangalbhaskar'

# ip=0.0.0.0
# port=4040
execstart_path=${_BZO__PYVENV_PATH}/bzo-v1/bin

${execstart_path}/uvicorn web_server_subapi:app --reload

cd -
