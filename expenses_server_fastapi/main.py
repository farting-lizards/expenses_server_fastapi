from fastapi import FastAPI
from expenses_server_fastapi.db import Base, engine
from .routes.accounts import router as account_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(account_router)