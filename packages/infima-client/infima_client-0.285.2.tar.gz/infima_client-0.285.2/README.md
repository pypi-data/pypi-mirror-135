# infima_client

A client library for accessing Infima. It will manage the HTTP REST requests for you.

## System requirements

The infima_client requires Python 3.7+. It is multi-platform, and the goal is to make
it work equally well on Windows, Linux and OSX.

## Installation

The library is published in PyPi.

```shell
pip install infima_client
```

## Usage

Contact [Support](support@infima.io) for an access token.

```python
from infima_client import InfimaClient

token = "..."
client = InfimaClient(token=token)
client.demo()
```

Alternatively, the token can be configured with the `INFIMA_TOKEN` environment variable.

## More Information

See the [Docs](http://docs.infima.io/) for more information.

Contact [Support](support@infima.io) if you have any questions.
