from sqlmodel import SQLModel


class LoginUserSchema(SQLModel):
    email: str
    password: str

class LoginOutputSchema(SQLModel):
    refresh_token: str
    access_token: str
    token_type: str