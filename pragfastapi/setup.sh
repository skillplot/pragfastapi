#!/bin/bash

## Copyright (c) 2020 mangalbhaskar.
# __author__='mangalbhaskar'

pdirs=(
  app
  app/api
  app/config
  app/db
  app/dnn/gpuconfig
  app/entities
  app/routes
  app/schemas
  app/_site/images
  app/templates/src
  app/utils
  app/tests
  docs
  test
  test/config
  data
)

for d in "${pdirs[@]}"; do
  echo "Creating directory: ${d}"
  mkdir -p ${d}
done
