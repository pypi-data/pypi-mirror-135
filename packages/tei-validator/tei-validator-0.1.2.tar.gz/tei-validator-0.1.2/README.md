# tei-validator

[![PyPI](https://img.shields.io/pypi/v/tei-validator.svg)](https://pypi.org/project/tei-validator/)

TEI XML validation package

## Installation

Install this library using `pip`:

    $ pip install tei-validator

## Usage

```shell
usage: tei-validator [-h] [--debug] [--output OUTPUT] [path]

positional arguments:
  path                  path or glob expression 

options:
  -h, --help            show this help message and exit
  --debug, -d           increases log level to debug
  --output OUTPUT, -o OUTPUT
                        saves the log output to a file
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

    cd tei-validator
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
