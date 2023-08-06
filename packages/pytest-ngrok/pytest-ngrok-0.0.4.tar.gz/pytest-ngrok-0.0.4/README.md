[![Documentation Status](https://readthedocs.org/projects/pytest-ngrok/badge/?version=latest)](https://pytest-ngrok.readthedocs.io/en/latest/?badge=latest)

[![ci](https://github.com/Apkawa/pytest-ngrok/actions/workflows/ci.yml/badge.svg)](https://github.com/Apkawa/pytest-django-ngrok/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/Apkawa/pytest-ngrok/branch/master/graph/badge.svg)](https://codecov.io/gh/Apkawa/pytest-ngrok) </br>

[![PyPi](https://img.shields.io/pypi/v/pytest-ngrok.svg)](https://pypi.python.org/pypi/pytest-ngrok)
[![PyPI Python versions](https://img.shields.io/pypi/pyversions/pytest-ngrok.svg)](https://pypi.python.org/pypi/pytest-ngrok)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)</br>

<!--
[![codecov](https://codecov.io/gh/Apkawa/pytest-ngrok/branch/master/graph/badge.svg)](https://codecov.io/gh/Apkawa/pytest-ngrok)
[![Requirements Status](https://requires.io/github/Apkawa/pytest-ngrok/requirements.svg?branch=master)](https://requires.io/github/Apkawa/pytest-ngrok/requirements/?branch=master)
[![PyUP](https://pyup.io/repos/github/Apkawa/pytest-ngrok/shield.svg)](https://pyup.io/repos/github/Apkawa/pytest-ngrok)
-->

pytest integration for [ngrok.io](https://ngrok.com/)

# Installation

from PyPi

```bash
pip install pytest-ngrok
```
or from git

```bash
pip install -e git+https://githib.com/Apkawa/pytest-ngrok.git#egg=pytest-ngrok
```


# Usage

```python
import pytest

from urllib.error import HTTPError
from urllib.request import urlopen

def test_ngrok(ngrok, httpserver):
    httpserver.expect_request("/foobar").respond_with_data("ok")
    remote_url = ngrok(httpserver.port)
    assert urlopen(remote_url + "/foobar").read() == b'ok'


def test_ngrok_context_manager(ngrok, httpserver):
    # example local server
    httpserver.expect_request("/foobar").respond_with_data("ok")
    with ngrok(httpserver.port) as remote_url:
        _test_url = str(remote_url) + '/foobar'
        assert urlopen(_test_url).read() == b'ok'

    # Connection closes
    pytest.raises(HTTPError, urlopen, _test_url)
```

With `pytest-django` can use fixture `live_server_ngrok`

```python
def test_server(live_server_ngrok):
    assert live_server_ngrok.url.endswith('ngrok.io')
```

# Contributing

## Initialize

```bash
python -m venv /tmp/.venv/pytest-ngrok
source /tmp/.venv/pytest-ngrok/activate
pip install -r requirements-dev.txt
```

## Run tests

```bash
pytest
tox
```

## Update version

```bash
python setup.py bumpversion
```

## Publish pypi

```bash
python setup.py publish
```
