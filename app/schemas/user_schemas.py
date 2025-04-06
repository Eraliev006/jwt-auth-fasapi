from sqlmodel import SQLModel


class __BaseUserSchema(SQLModel):
    name: str
    email: str
    avatar_url: str

class CreateUserSchema(__BaseUserSchema):
    password: str

class OutputUserSchema(__BaseUserSchema):
    id: int
    is_verified: bool

