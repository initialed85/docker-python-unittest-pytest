#!/usr/bin/env bash

docker build -t test_some_module -f Dockerfile .

exit ${?}
