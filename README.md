# docker-python-unittest-pytest

This repository demonstrates a simple `Python` module with some unit tests using `unittest` and `pytest`; it also demonstrates that using Docker and a multi-stage `Dockerfile`.

The multi-stage `Dockerfile` is completely unnecessary, but it demonstrates an approach that can be used to build `C++` libraries that require a large build environment but a small run environment. 

## Steps to run the tests natively on your machine

**Prerequisites**:

- Python 3
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
    - `pip install virtualenvwrapper`
    - `source /usr/local/bin/virtualenvwrapper.sh`

**Steps**:

- Create a Python3 Virtualenv
    - ```mkvirtualenv -p `which python3` unittest-pytest```
- Ensure that Virtualenv is activated
    - `workon unittest-pytest` 
- Install the dev/test requirements
    - `pip install -r requirements-dev.txt`
- Run the tests
    - `python -m pytest -v --junit-xml test_results.xml some_module`
- View the test results (in JUnit XML)
    - `cat test_results.xml`

## Steps to run the tests in Docker

**Prerequisites**:

- Docker

**Steps**:

- Build the Docker image
    - `docker build -t test_some_module -f Dockerfile .`
- Create a container instance of that image (which will run the entrypoint)
    - `docker run -it --name test_some_module test_some_module`
- Copy out the test results
    - `docker cp test_some_module:/srv/test_results.xml ./test_results.xml`
- Remove the container instance
    - `docker rm -f test_some_module`
- View the test results (in JUnit XML)
    - `cat test_results/some_module_results.xml`

## Convenience scripts (for Docker approach)

- Build the Docker image
    - `./build.sh`
- Run the Docker image and extract the test results
    - `./test.sh`
