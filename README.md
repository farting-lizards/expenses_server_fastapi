# Expenses Server in FastAPI

# Development

1. Start the db:
```sh
sudo docker compose -f docker-compose.yml -p expenses_server up
```

2. Create the db tables and seed categories/accounts (only needed on a fresh db):
```sh
poetry run alembic upgrade head
```

3. Create a `.env` file with the JWT signing key:
```sh
python3 -c "import secrets; print(f'JWT_ENCODE_KEY={secrets.token_hex(32)}')" > .env
```

4. Create a user for logging in:
```sh
poetry run python -c "from expenses_server.utils import create_user; create_user('your-username')"
```

5. Start the server on port 8090:
```sh
poetry run uvicorn expenses_server.main:app --reload --port=8090 --use-colors
```

6. Running tests

```sh
poetry run pytest # runs all tests
poetry run pytest -s --pdb # helpful for debugging tests
```

7. Kill the containers and remove volumes

```sh
sudo docker compose -f docker-compose.yml -p expenses_server down --remove-orphans --volumes
```
