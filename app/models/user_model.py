from sqlmodel import SQLModel, Field


class User(SQLModel, table = True):
    id: int | None = Field(primary_key=True, nullable=False, default=None)
    name: str
    password_hash: str
    email: str
    avatar_url: str





