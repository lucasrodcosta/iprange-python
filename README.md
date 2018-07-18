[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/iprange-python.svg)](https://badge.fury.io/py/iprange-python)

# IPRange

Store IP Ranges in Redis as sorted sets for fast retrieval

## Installation

    pip install iprange-python

## Usage

```python
from iprange import IPRange

iprange = IPRange()

# Add a new range with some metadata
iprange.add('192.168.0.1/24', {'some': 'data', 'more': 'metadata'})

# Find the most specific range that contains a specific IP
iprange.find('192.168.0.20')
# => {'range': '192.168.0.1/24', 'some': 'data', 'more': 'metadata'}

# Find all ranges that contains a specific IP
iprange.find_all('192.168.0.20')
# => [{'range': '192.168.0.1/24', 'some': 'data', 'more': 'metadata'}]

# Delete the range
iprange.remove('192.168.0.1/24')
```

You can use it with Redis Cluster too:

```python
from iprange import IPRange

# Requires at least one node for cluster discovery. Multiple nodes is recommended.
startup_nodes = [{'host': '127.0.0.1', 'port': 16379}]
iprange = IPRange(redis_cluster=True, startup_nodes=startup_nodes)

# ...
```

## IPRange in other languages

- [Ruby](https://github.com/globocom/iprange)

## Notice

This library relies on [a Redis fork that implements interval sets](https://github.com/hoxworth/redis/tree/2.6-intervals),
as described in this [blog post](http://blog.togo.io/how-to/adding-interval-sets-to-redis/).

You can also use [a more recent version of Redis with Interval Sets](https://github.com/lucasrodcosta/redis).
