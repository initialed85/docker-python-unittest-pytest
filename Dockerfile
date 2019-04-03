FROM ubuntu:16.04

# copy in the software
ADD requirements.txt /srv/requirements.txt
ADD requirements-dev.txt /srv/requirements-dev.txt
ADD some_module /srv/some_module

# install the prerequisites
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /srv/

# install the requirenents
RUN pip3 install -r requirements-dev.txt

# Build our entrypoint
RUN echo "#!/usr/bin/env bash" > test.sh
RUN echo "python3 -m pytest -v --junit-xml test_results/some_module_results.xml some_module" >> test.sh
RUN chmod +x test.sh

# Run the entrypoint (only when the image is instantiated into a container)
CMD ["./test.sh"]

# to build: docker build -t test_some_module .

# to run: docker run --name test_some_module test_some_module

# once the run is complete, /srv/test_results inside the container will hold JUnit XML files
