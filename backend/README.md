```bash
$ pylint *.py
```

App required next dependencies:
- aiohttp
- aiohttp-devtools
- sqlalchemy
- psycopg2-binary
- asyncpg
- pydantic
- pydantic[Email]
- pika
- python-dotenv
- passlib
- pyjwt

Init:
```bash
cd backend
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Run server:
```bash
# if clear db run alembic:
alembic upgrade head

# run server
python main.py
```

Run live reload:
```bash
adev runserver main.py --port=8080
```
