# docker-python-unittest-pytest

## Prerequisites

- Python 3
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
    - `pip install virtualenvwrapper`
    - ```source /usr/local/bin/virtualenvwrapper.sh```
- (optional) [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

## Steps to run the tests

- Create a Python3 Virtualenv
    - ```mkvirtualenv -p `which python3` unittest-pytest```
- Ensure that Virtualenv is activated
    - `workon unittest-pytest` 
- Install the dev/test requirements
    - `pip install -r requirements-dev.txt`
- Run the tests
    - `mkdir -p test_results`
    - `python -m pytest -v --junit-xml test_results/some_module_results.xml some_module`
- View the test results (in JUnit XML)
    - `cat test_results/some_module_results.xml`

## Steps to run the tests in Docker

- Build the Docker image
    - `docker build -t test_some_module .`
- Create a container instance of that image (which will run the entrypoint)
    - `docker run --name test_some_module test_some_module`
- Copy out the test results
    - `docker cp test_some_module:/srv/test_results .`
- Remove the container instance
    - `docker rm test_some_module`
- View the test results (in JUnit XML)
    - `cat test_results/some_module_results.xml`
