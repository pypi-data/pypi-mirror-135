# Psycopg2 Error Handler

## Getting started
### Motivation
There is a need to catch errors caused by the database.
However, psycopg2 does not provide any mechanisms for catching errors.

`psycopg2_error_handler` provides list of exceptions (gathered form psycopg2) and decorator for handling errors.

### Installation
```bash
pip install psycopg2-error-handler
```

### Usage
Async usage with `aiopg`.
```python
from psycopg2_error.handler import psycopg2_error_handler
from psycopg2_error.errors import UniqueViolation, DatabaseError

async def create_user(payload):
    stmt = User.insert().values(payload)
    try:
        await execute(stmt)
    except UniqueViolation:
        do_somthing_grate_when_user_already_exists()
    except DatabaseError:
        handler_another_errors()

@psycopg2_error_handler
async def execute(stmt):
    async with engine.acquire() as conn:
        return await conn.execute(stmt)
```

Sync usage
```python
def create_user(payload):
    stmt = User.insert().values(payload)
    try:
        execute(stmt)
    except UniqueViolation:
        do_somthing_grate_when_user_already_exists()
    except DatabaseError:
        handler_another_errors()

@psycopg2_error_handler
def execute(stmt):
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()
```