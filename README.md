# Read data from Pure Energy api

Use the code in this project to read data from the customer api provided by
[Pure Energie](https://pure-energie.nl/)

## Install

Requirements:

- python3
- account at Pure Energie

Create a file named `pesConfig.json` (pes is short for Pure Energie Slurper) in your home folder. It's content should
look like this:

```json
{
  "email": "YOUR EMAIL",
  "password": "YOUR PASSWORD",
  "connection_id": "YOUR CONNECTION_ID",
  "access_token": "YOUR ACCESS_TOKEN",
  "start_of_data": "YYYY-MM-DD"
}
```

`email` and `password` are the credentials you use to log in.

Get the values for connection_id and access_token from the browser's network inspector.
`connection_id` is part of the url and `access_token` is actually named `X-token` and is returned as a header.

`start_of_date` is the date of the first measurements in your account.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

TODO

- Run in the afternoon because that's when yesterday's data becomes available. If run too early, the code will fail (
  TODO: fix this)

## Test

```bash
python3 -m pytest
```

## Dev todo

done - cmd line tool support
- reload
done - get rid of files,
done - append
done - print graphs
- improve test-ability and test coverage
- fix error (?) when data not yet available, warning maybe?
done - move credentials file to a safer place
- website
  - dashboard with 7 days graph? 

Tests with mocks:

https://pytest-with-eric.com/mocking/pytest-mocking/