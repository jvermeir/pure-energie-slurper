# Scala version of PES

## Database with docker compose

```bash
docker compose up
```

Start mysql tool

```bash
docker exec -it [container id here] /bin/bash
```

Create table

```sql
use verbruik;

create table verbruik_per_uur 
(
    period varchar(100) not null , 
    total_usage float, 
    redelivery float,
    CONSTRAINT PK_period PRIMARY KEY (period)
);
```

## Database, the hard way

```bash
docker run --rm -v "$PWD/data":/var/lib/mysql --user 1000:1000 --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -p 3306:3306 -d mysql:latest
```

copy a file named [enable-mysql-native-password.cnf](data%2Fenable-mysql-native-password.cnf) in `/data/`

contents:

```
[mysqld]
mysql_native_password=ON
```

Restart the container.

```bash
docker exec -it [container id here] /bin/bash
```

At the prompt:
```bash
mysql -u root -p
```

enter the password set in `MYSQL_ROOT_PASSWORD` (see commandline above)

Create database and account data:

```bash
create database verbruik;
create user 'verbruik'@'%' identified by 'verbruik';
grant all on verbruik.* to 'verbruik'@'%';
```

Exit the tool and start again:

```bash
mysql -u verbruik -p
```

Create the table

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

update data from Pure Energie site for January 2017

```bash
curl -v -d '{"startDate":"2017-01-01", "endDate": "2017-02-01"}' \
-H 'Content-Type: application/json' \
-X POST localhost:8080/refresh
```

load data

```bash
curl -v  -H 'Content-Type: application/json' localhost:8080/verbruik/2017-02-01/2017-02-02
```