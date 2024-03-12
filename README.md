# Expenses Server in FastAPI

# Development

1. Start the db:
```sh
 sudo docker-compose -f docker-compose.yml -p expenses_server_fastapi up
```

2. Start the server on port 8090:
```sh
poetry run uvicorn expenses_server_fastapi.main:app --reload --port=8090 --use-colors
```
