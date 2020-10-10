#!/bin/bash

## Copyright (c) 2020 mangalbhaskar.
# __author__='mangalbhaskar'

# ip=0.0.0.0
# port=4040
execstart_path=${_BZO__PYVENV_PATH}/bzo-v1/bin

${execstart_path}/uvicorn web_server_redisqueue:app --reload

cd -


# ## https://medium.com/@mike.p.moritz/using-docker-compose-to-deploy-a-lightweight-python-rest-api-with-a-job-queue-37e6072a209b


docker build -t myproj:latest .
docker run --name myproj -p 5057:5057 --rm myproj:latest


# docker build -t myproj:latest .
# docker-compose -f docker-compose.yml up

curl -v -X POST http://localhost:5057/groups/group1 -d '{"owner": "foo", "description": "bar"}'
