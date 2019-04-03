# docker-python-unittest-pytest

## Prerequisites

- Python 3
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
    - `pip install virtualenvwrapper`
    - ```source /usr/local/bin/virtualenvwrapper.sh``` 

## Steps to run the tests

- Create a Python3 Virtualenv
    - ```mkvirtualenv -p `which python3` unittest-pytest```
- Ensure that Virtualenv is activated
    - `workon unittest-pytest` 
- Install the dev/test requirements
    - `pip install -r requirements-dev.txt`
- Run the tests
    - `python -m pytest -v --junit-xml test_results/some_module_results.xml some_module`
- To view the test results (in JUnit XML)
    - `cat test_results/some_module_results.xml`
