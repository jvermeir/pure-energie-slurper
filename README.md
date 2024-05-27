# Read data from Pure Energy api

Use the code in this project to read data from the customer api provided by 
[Pure Energie](https://pure-energie.nl/)

## Install

Requirements:

- python3
- account at Pure Energie

Create a file named `properties.json` in your home folder. It's content should look like this:

```json
{"email": "YOUR EMAIL", "password": "YOUR PASSWORD", "connection_id":  "YOUR CONNECTION_ID", "access_token":  "YOUR ACCESS_TOKEN"}
```

Get the values for connection_id and access_token from the browser's network inspector.
`connection_id` is part of the url and `access_token` is actually named `X-token` and is returned as a header.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

TODO
- Run in the afternoon because that's when yesterday's data becomes available. If run too early, the code will fail (TODO: fix this)

## Test

```bash
python3 -m pytest
```

## Dev todo

- cmd line tool support
- reload
- append
- print graphs
- website
- improve test-ability and  test coverage
- move credentials file to a safer place