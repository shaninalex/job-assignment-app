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
uvicorn main:app --port=8080
# or using fastapi cli on production mode
fastapi run main.py --port=8080
```

Run dev live reload:

```bash
fastapi dev main.py --port=8080
# or
uvicorn main:app --reload --port=8080
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

# back to the backend folder
cd ./backend/

# apply alembic migrations into test database
# alembic --name alembic_test upgrade head
# NOTE: no need to do that, since tests create all tables by Base.metadata.create_all
# and clear tables after tests

# run tests
pytest --verbose --cov=app
```
