#!/bin/bash

## Copyright (c) 2020 mangalbhaskar.
# __author__='mangalbhaskar'

# ip=0.0.0.0
# port=4040
execstart_path=${_BZO__PYVENV_PATH}/bzo-v1/bin

${execstart_path}/uvicorn web_server_ipcam:app --reload --port 4040

cd -

# https://medium.com/swlh/real-time-object-detection-deployment-using-tensorflow-keras-and-aws-ec2-instance-1c1937c001d9?
# sudo apt-get update
# sudo apt install python3-pip
# sudo apt-get install libsm6 libxrender1 libfontconfig1 libice6 nginx gunicorn
# pip3 install uvicorn==0.11.1 cvlib==0.2.3 starlette==0.12.9 opencv_python==4.1.2.30 pydantic==1.3 Pillow==7.0.0 fastapi==0.45.0 numpy==1.18.1 tensorflow gevent
