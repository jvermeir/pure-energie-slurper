# Scala version of PES

## Database

start container to create a mysql database named `db_example` 

```bash
# in src/main/docker
docker-compose up
```

create a table with the mysql tool in the container

```bash
mysql --host=localhost --user=springuser --password=ThePassword db_example
```

```sql
create table verbruik_per_uur 
(
    period varchar(100) not null , 
    total_usage float, 
    redelivery float,
    CONSTRAINT PK_period PRIMARY KEY (period)
);
```

## Test REST interface

update data from Pure Engergie site for January 2017

```bash
curl -v -d '{"startDate":"2017-01-01", "endDate": "2017-02-01"}' \
-H 'Content-Type: application/json' \
-X POST localhost:8080/refresh
```
