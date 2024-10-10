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

## Tests

```bash
# to run test first need to start test environment

# back in project root folder
cd ../  

# stop dev containers
make stop

# start test container
make test_start

cd ./backend/

# apply alembic migrations into test database
# alembic --name alembic_test upgrade head

# run tests
pytest --verbose --cov=app
```