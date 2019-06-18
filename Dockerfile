#
# ---- builder
#

FROM ubuntu:16.04 AS builder

# install the prerequisites
RUN apt-get update && apt-get install -y python3 python3-pip

# copy in the requirements
COPY requirements.txt /srv/requirements.txt
COPY requirements-dev.txt /srv/requirements-dev.txt

# create a folder to hold the downloaded/built requirements
RUN mkdir -p /srv/some_module

# install the requirenents to that folder
RUN pip3 install -r /srv/requirements-dev.txt --target /srv/some_module

#
# ---- test runner
#

FROM ubuntu:16.04

# install the prerequisites (note: only python, no pip)
RUN apt-get update && apt-get install -y python3

# copy the requirements from the builder stage
COPY --from=builder /srv/some_module /srv/some_module

# copy in the code to be tested (this merges with the folder above)
COPY some_module /srv/some_module

# change to the appropriate folder
WORKDIR /srv/some_module

# run the entrypoint (only when the image is instantiated into a container)
CMD python3 -m pytest -v --junit-xml /srv/test_results.xml some_module_test.py

#
# ---- how to use
#

# to build (-t is image name, -f is Dockerfile path, . is the context folder)
# docker build -t test_some_module -f Dockerfile .

# to run (-it is interactive terminal for colours etc, --name is the container nane, test_some_module is the image name)
# docker run -it --name test_some_module test_some_module

# to get the results (test_some_module:/srv/test_results.xml is the container path, ./test_results.xml is the local path)
# docker cp test_some_module:/srv/test_results.xml ./test_results.xml

# to remove the container (not the image)
# docker rm -f test_some_module
