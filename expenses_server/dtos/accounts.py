from pydantic import BaseModel


class Account(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
