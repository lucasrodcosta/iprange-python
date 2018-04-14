[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# IPRange

Store IP Ranges in Redis as sorted sets for fast retrieval

## Installation

    pip install iprange-python

## Usage

    >>> from iprange import IPRange
    >>> iprange = IPRange()
    >>> iprange.add('192.168.0.1/24', {'some': 'data', 'more': 'metadata'})
    >>> iprange.find('192.168.0.20')
    {'range': '192.168.0.1/24', 'some': 'data', 'more': 'metadata'}

## IPRange in other languages

- [Ruby](https://github.com/globocom/iprange)

## Notice

This library relies on [a Redis fork that implements interval sets](https://github.com/hoxworth/redis/tree/2.6-intervals),
as described in this [blog post](http://blog.togo.io/how-to/adding-interval-sets-to-redis/).

You can also use [a more recent version of Redis with Interval Sets](https://github.com/lucasrodcosta/redis).
