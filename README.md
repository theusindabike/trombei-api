# Trombei API project



## Pre-req
[Docker & Compose](https://docs.docker.com/compose/install/)

## First Access
```console
git clone git@github.com:theusindabike/trombei-api.git
cd trombei-api
cp contrib/env-sample .env
```

## Developing

### Local Runserver:
```commandline
make run
```
### Tests
```commandline
make tests
```

## Run with Gunicorn, Nginx and Postgres
```commandline
make run_staging
```

## Open API
Available in http://127.0.0.1/swagger/ and http://127.0.0.1/redoc/



## Built With
1. docker-compose
2. django
3. postgres


