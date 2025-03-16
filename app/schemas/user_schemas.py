from sqlmodel import SQLModel


class BaseUserSchema(SQLModel):
    name: str
    email: str
    avatar_url: str

class CreateUserSchema(BaseUserSchema):
    password: str

class OutputUserSchema(BaseUserSchema):
    id: int
    is_verified: bool
