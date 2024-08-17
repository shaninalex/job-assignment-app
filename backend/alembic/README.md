Generic single-database configuration.

```bash
# on clear db
alembic upgrade head

# on new changes to model
alembic revision --autogenerate -m "initial"
````
