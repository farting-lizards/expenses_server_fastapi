from pydantic import UUID4, BaseModel


class User(BaseModel):
    id: UUID4
    username: str


class UserToken(BaseModel):
    access_token: str
    token_type: str
