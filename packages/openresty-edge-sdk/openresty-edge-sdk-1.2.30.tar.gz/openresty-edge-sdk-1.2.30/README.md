# OpenResty Edge SDK


### Introduction

Python SDK of [OpenResty Edge](https://openresty.com/en/edge/), which provides users with the ability to write custom tools to use OpenResty Edge.

### Installation

```
pip install openresty-edge-sdk
```

### Usage
```python

from edge2client import Edge2Client

client = Edge2Client('http://127.0.0.1:8080', 'username', 'password')
client.login()
app_id = client.new_app(domains = ['orig.foo.com'], label = 'origin site for foo.com')

print(app_id)
```
