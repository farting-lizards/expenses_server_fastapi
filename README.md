# Expenses Server in FastAPI

# Development

1. Start the db:
```sh
sudo docker compose -f docker-compose.yml -p expenses_server up
```

2. Start the server on port 8090:
```sh
poetry run uvicorn expenses_server.main:app --reload --port=8090 --use-colors
```

3. Running tests

```sh
poetry run pytest # runs all tests
poetry run pytest -s --pdb # helpful for debugging tests
```

4. Kill the containers and remove volumes

```sh
sudo docker compose -f docker-compose.yml -p expenses_server down --remove-orphans --volumes
```
