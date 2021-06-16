<h1 align="center" style="font-size: 3rem; margin: -15px 0">
DOLib
</h1>

---

[![PyPI version](https://badge.fury.io/py/dolib.svg)](https://badge.fury.io/py/dolib)
![Supported Python Versions](https://img.shields.io/pypi/pyversions/dolib)
![Tests](https://github.com/geraxe/dolib/workflows/Tests/badge.svg)
[![Coverage](https://codecov.io/gh/geraxe/dolib/branch/master/graph/badge.svg)](https://codecov.io/gh/geraxe/dolib)


DOLib is a fully featured python 3.6+ library for Digital Ocean, which provides sync and async APIs. This library supports all Digital Ocean API methods and simple in use. Enjoy!

You can easily use the sync Client

```pycon
>>> from dolib import Client
>>> client = Client(token="60c13d47***ed98dd9")
>>> droplet = client.droplets.all()[0]
>>> droplet
Droplet(id=120794777, name='dolib-test', region=Region(fra1),
  size=Size(s-2vcpu-4gb), image=Image('18.04 x64'), ....)

>>> volume = client.volumes.get("53cf7120-9d5b-11ea-aed1-0a58ac14d008")
>>> client.volumes.attach(volume, droplet_id=droplet.id)
```

Or, using the async client

```pycon
>>> from dolib import AsyncClient
>>> from dolib.models import Droplet

>>> async with Client(token="60c13d47***ed98dd9") as client:
...   droplet = Droplet(
...     name="dolib-droplet",
...     region="fra1",
...     size="s-1vcpu-1gb",
...     image="ubuntu-18-04-x64")
...   droplet = await client.droplets.create(droplet)
>>> droplet
Droplet(id=120794777, name='dolib-droplet', region=Region(fra1),
  size=Size(s-1vcpu-1gb), image=Image('18.04 x64'), ....)
```


## Features

DOLib supports all Digital Ocean API methods (https://developers.digitalocean.com/documentation/v2/)

You can easily:

* Create droplets and manage it
* Make volumes and attach it to droplets
* Create Kubernetes clusters and manage it
* Operate with managed databases
* and more more more

## Dependencies

The DOLib uses this awesome projects:

* `httpx` - for http interaction with DO API
* `pydantic` - for model defenition and serialization


## Installation

Easy install from PyPI:

```bash
pip install dolib
```

*dolib* required python 3.6, 3.7, 3.8, or 3.9, [pydantic](https://pypi.org/project/pydantic/), and
[`httpx`](https://pypi.org/project/httpx/)
