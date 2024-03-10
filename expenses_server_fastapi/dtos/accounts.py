from pydantic import UUID4, BaseModel

class Account(BaseModel):
    id: UUID4
    name: str

    class Config:
        from_attributes = True