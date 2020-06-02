# Python Digital Ocean Library

[![PyPI version](https://badge.fury.io/py/dolib.svg)](https://badge.fury.io/py/dolib)
![Supported Python Versions](https://img.shields.io/pypi/pyversions/dolib)
![Tests](https://github.com/geraxe/dolib/workflows/Tests/badge.svg)
[![Coverage](https://codecov.io/gh/geraxe/dolib/branch/master/graph/badge.svg)](https://codecov.io/gh/geraxe/dolib)

## Description

DOLib is a fully featured python 3.6+ library for Digital Ocean, which provides sync and async APIs. This library supports all Digital Ocean API methods and simple in use. Enjoy!

## Documentation

Comming soon.

## Requirements

Python 3.6+

DOLib uses these awesome libraries:

* <a href="https://requests.readthedocs.io/" class="external-link" target="_blank">Requests</a> for network.
* <a href="https://www.python-httpx.org/" class="external-link" target="_blank">HTTPX</a> for async network.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> for the data parts.

## Installation

```shell
pip install dolib
```

## Example

Sync client
```Python
from dolib import Client

client = Client(token="60c13d47f17dbed9f7293cf8c82d18fece3439a54f88e6c52c2df07f87bd8dd9")

droplets = client.droplets.all()
volume = client.volumes.get("53cf7120-9d5b-11ea-aed1-0a58ac14d008")

client.volumes.attach(volume, droplet_id=droplets[0].id)
```

Async client
```Python
from dolib import AsyncClient
from dolib.models import Droplet

async with Client(token="60c13d47f17dbed9f7293cf8c82d18fece3439a54f88e6c52c2df07f87bd8dd9") as client:
    droplet = Droplet(name="dolib-droplet", region="fra1", size="s-1vcpu-1gb", image="ubuntu-18-04-x64")
    droplet = await client.droplets.create(droplet)

```




## Contributing

To run the tests:

```shell
tox -p all
```

## Versioning

This project follows [Semantic Versioning 2.0.0](http://semver.org/spec/v2.0.0.html).

## License

This project is licensed under the terms of the MIT license.
