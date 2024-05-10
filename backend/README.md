# Example backend

This is my old [aiohttp generic webservice template](https://github.com/shaninalex/generic-service) .

To run database do this command:
```bash
docker compose -f docker-compose.dev.yml up -d --build
```

Then create python virtual env, install dependencies, init db schema and run application:

```bash

#1
python3 -m venv env

#1.1 - activate virtual environment
source env/bin/activate

#2
pip install -r requirements.txt

#3
python init.py

#4
python app.py

```
