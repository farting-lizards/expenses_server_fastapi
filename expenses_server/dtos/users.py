from pydantic import UUID4, BaseModel, ConfigDict


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    username: str


class UserToken(BaseModel):
    access_token: str
    token_type: str
