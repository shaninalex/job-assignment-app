Generic single-database configuration.


operations
```bash
# on clear db
alembic upgrade head

# on new changes to model
alembic revision --autogenerate -m "initial"
````

```sql
-- able to use UUID as an primary key
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```
