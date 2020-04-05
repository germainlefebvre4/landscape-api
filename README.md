# Landscape Api

## Prerequisite
Python versions covered:
* `Python 3.6`
* `Python 3.7`
* `Python 3.8`

## Getting started
### Init database
```sh
pipenv run flask init-db
```
### Run the app
```sh
pipenv run flask run --host=0.0.0.0 --port=8080
```
Browse the app on localhost port 8080.

## Pipenv
### Prepare
```sh
pipenv update
```

### Runtime
```sh
pipenv run python main.py
```

### Systemd service
```
[Unit]
Description=Landscape API Service
After=multi-user.target

[Service]
User=root
WorkingDirectory=/opt/python/landscape-api
Restart=always
Type=simple
ExecStart=/usr/local/bin/pipenv run python main.py
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
```
