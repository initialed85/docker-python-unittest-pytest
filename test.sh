#!/usr/bin/env bash

docker run -it --name test_some_module test_some_module
RETVAL=${?}

docker cp test_some_module:/srv/test_results.xml ./test_results.xml

docker rm -f test_some_module

ls -al ./test_results.xml

exit ${RETVAL}
