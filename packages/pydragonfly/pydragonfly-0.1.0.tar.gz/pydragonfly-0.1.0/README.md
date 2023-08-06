# pyDragonfly

[![PyPI version](https://badge.fury.io/py/pydragonfly.svg)](https://badge.fury.io/py/pydragonfly)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/pydragonfly.svg)](https://pypi.python.org/pypi/pydragonfly/)

[![Linter & Tests](https://github.com/certego/pydragonfly/workflows/Linter%20&%20Tests/badge.svg)](https://github.com/certego/pydragonfly/actions)
[![codecov](https://codecov.io/gh/certego/pydragonfly/branch/main/graph/badge.svg?token=KBk4rQj08b)](https://codecov.io/gh/certego/pydragonfly)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/certego/pydragonfly.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/certego/pydragonfly/context:python)
[![CodeFactor](https://www.codefactor.io/repository/github/certego/pydragonfly/badge)](https://www.codefactor.io/repository/github/certego/pydragonfly)

Robust Python **SDK** and **Command Line Client** for interacting with Certego's [Dragonfly](https://dragonfly.certego.net/) service's API. Built with [django-rest-client](https://github.com/certego/django-rest-client).

## Features

- Easy one-time configuration with self documented help and hints along the way.
- Supports all endpoints of [Dragonfly's REST API](https://dragonfly.certego.net/api/schema/swagger-ui/).
- Analysis:
  - Create new analysis by uploading sample
  - Revoke a running analysis
  - View analysis report
  - List latest with filtering, ordering, pagination capabilities
  - Download sample of an existing analysis
- Profile and Rule:
  - Create new Profile or Rule objects
  - Update existing Profile and Rule objects
  - List latest with filtering, ordering, pagination capabilities
- View and manage your dragonfly organization and invitations
- View and manage active browser sessions
- View account access and subscription info

## Demo

[![pydragonfly asciicast](https://asciinema.org/a/443248.svg)](https://asciinema.org/a/443248)

## Installation

Requires python version >=3.6.

```bash
$ pip3 install pydragonfly
```

For development/testing, `pip3 install pydragonfly[dev]`

## Documentation

[![Documentation Status](https://readthedocs.com/projects/certego-pydragonfly/badge/?version=latest&token=ab49e3570b3dd2c9e750976bf2d32ffb505f6a1b573b5657470ad2e4e372e684)](https://certego-pydragonfly.readthedocs-hosted.com/en/latest/?badge=latest)

- Documentation: https://certego-pydragonfly.readthedocs-hosted.com/
- Changelog: [CHANGELOG.md](https://github.com/certego/pydragonfly/blob/master/.github/CHANGELOG.md)

## FAQ

#### Generate API key

You need a valid API key to interact with the Dragonfly server. For this,
head on over to https://dragonfly.certego.net/me/sessions and click on the `Generate +` button.
