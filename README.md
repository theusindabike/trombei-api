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

### Run local with Django runserver:
```commandline
make run
```
### Tests
```commandline
make tests
```

### Lint (flake8)
```commandline
make lint
```

## Run with Gunicorn, Nginx and Postgres
```commandline
make run_staging
```

## Open API
Available at: http://localhost/swagger/ and http://localhost/redoc/


## Simulating Google OAuth Login via Web
1. Access
    ```console
    https://accounts.google.com/o/oauth2/v2/auth?client_id=<<GOOGLE_OAUTH2_LOGIN_CLIENT_ID>>&response_type=code&scope=openid%20email%20profile&access_type=offline&redirect_uri=<<CALLBACK_URL>>
    ```
2. Copy the returned **Code** in url param<br />
3. Make a POST to http://localhost/api/v1/oauth/google passing that **Code**, for example: <br />
    ```console
    curl --data "code=4/0aaabbb7ZThsWhHh9zB93MiinOAaSFcKsPdwXdYy_NkpqC8xAOclp33F1_0zK4P9fU9Wzzzz" https://trombei.com/api/v1/oauth/google/
    ```
4. Now you should have a Token <br />
5. Finnaly, you can access a protected endpoint with that token as Authorization Header, for example: <br />
    ```console
    curl -H "Authorization: Token 123499d1c57d1d4e456c6009416b8a089cfa789" http://localhost/api/v1/users/me/
    ```



## Built with
1. docker-compose
2. django
3. postgres


