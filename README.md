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
  "start_of_data": "YYYY-MM-DD",
  "influx_url" : "http://localhost:8086", 
  "influx_token" : "YOUR TOKEN", 
  "influx_org" : "YOUR ORG ID", 
  "influx_bucket" : "verbruikbucket",
  "influx_enabled": false
}
```

`email` and `password` are the credentials you use to log in at Pure Engerie.

Get the values for connection_id and access_token from the browser's network inspector.
`connection_id` is part of the url and `access_token` is actually named `X-token` and is returned as a header.

`start_of_data` is the date of the first measurements in your account.

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
done - website
  - dashboard in influxdb 

## Influx

Experiment with InfluxDB as a database and using its dashboard to show graphs.

Note: use the 'influx_enabled' property to enable or disable influx.

### Docker 

see https://hub.docker.com/_/influxdb/
and https://docs.influxdata.com/influxdb/cloud/get-started/

Run influx container or influx/grafana using [docker compose](./docker/docker-compose.yml)  

```bash
docker run -d -p 8086:8086 \
    -v "$PWD/data:/var/lib/influxdb2" \
    -v "$PWD/config:/etc/influxdb2" \
    influxdb:2
```

setup database, run this once

```bash 
curl http://localhost:8086/api/v2/setup \
  --data '{
            "username": "admin",
            "password": "{replace}",
            "token": "{replace}",
            "bucket": "verbruikbucket",
            "org": "thuis"
        }'
```

create all access api token:

```bash
export INFLUX_HOST=http://localhost:8086
export INFLUX_ORG_ID={replace}
export INFLUX_TOKEN={replace}

curl --request POST \
"$INFLUX_HOST/api/v2/authorizations" \
  --header "Authorization: Token $INFLUX_TOKEN" \
  --header "Content-Type: text/plain; charset=utf-8" \
  --data '{
    "status": "active",
    "description": "All access token for get started tutorial",
    "orgID": "'"$INFLUX_ORG_ID"'",
    "permissions": [
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "authorizations"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "authorizations"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "buckets"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "buckets"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "dashboards"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "dashboards"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "orgs"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "orgs"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "sources"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "sources"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "tasks"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "tasks"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "telegrafs"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "telegrafs"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "users"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "users"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "variables"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "variables"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "scrapers"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "scrapers"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "secrets"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "secrets"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "labels"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "labels"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "views"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "views"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "documents"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "documents"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "notificationRules"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "notificationRules"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "notificationEndpoints"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "notificationEndpoints"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "checks"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "checks"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "dbrp"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "dbrp"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "notebooks"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "notebooks"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "annotations"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "annotations"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "remotes"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "remotes"}},
      {"action": "read", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "replications"}},
      {"action": "write", "resource": {"orgID": "'"$INFLUX_ORG_ID"'", "type": "replications"}}
    ]
  }
'
```

context for scripts

```bash 
export INFLUX_HOST=http://localhost:8086
export INFLUX_ORG=thuis
export INFLUX_ORG_ID={replace}
export INFLUX_TOKEN={replace}
```

### Sample curls

add `get-started` bucket 

```bash 
curl --request POST \
"$INFLUX_HOST/api/v2/buckets" \
  --header "Authorization: Token $INFLUX_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "orgID": "'"$INFLUX_ORG_ID"'",
    "name": "get-started",
    "retentionRules": [
      {
        "type": "expire",
        "everySeconds": 0
      }
    ]
  }'
```

list buckets

```bash 
curl --request GET \
"$INFLUX_HOST/api/v2/buckets" \
  --header "Authorization: Token $INFLUX_TOKEN"
```

select data from test dataset:

```bash
curl --get "$INFLUX_HOST/query?org=$INFLUX_ORG&bucket=get-started" \
  --header "Authorization: Token $INFLUX_TOKEN" \
  --data-urlencode "db=get-started" \
  --data-urlencode "rp=autogen" \
  --data-urlencode "q=SELECT co,hum,temp,room FROM home WHERE time >= '2022-01-01T08:00:00Z' AND time <= '2022-01-01T20:00:00Z'"
```

delete data

```bash 
curl --request POST http://localhost:8086/api/v2/delete?org=$INFLUX_ORG&bucket=verbruikbucket \
  --header "Authorization: Token $INFLUX_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{
    "start": "1720-03-01T00:00:00Z",
    "stop": "2261-04-11T23:47:16Z"
    }'
```
