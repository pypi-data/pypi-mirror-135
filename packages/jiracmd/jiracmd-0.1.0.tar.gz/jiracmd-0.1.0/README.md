# jiracmd

[![PyPI](https://img.shields.io/pypi/v/jiracmd.svg)](https://pypi.org/project/jiracmd/)
[![Changelog](https://img.shields.io/github/v/release/rfsantanna/jiracmd?include_prereleases&label=changelog)](https://github.com/rfsantanna/jiracmd/releases)
[![Tests](https://github.com/rfsantanna/jiracmd/workflows/Test/badge.svg)](https://github.com/rfsantanna/jiracmd/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/rfsantanna/jiracmd/blob/master/LICENSE)

Jira Command Line Tool

## Installation

Install this tool using `pip`:

    $ pip install jiracmd

## Usage

Usage instructions go here.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd jiracmd
    python -m venv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
