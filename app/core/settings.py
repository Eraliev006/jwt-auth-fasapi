from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class DBSettings(BaseModel):
    db_url: str

class SMTPSettings(BaseModel):
    sender_email: str
    smtp_server: str
    smtp_port: int
    smtp_login: str
    smtp_password: str

class RedisSettings(BaseModel):
    redis_host: str
    redis_port: int

class JWTSettings(BaseModel):
    secret_key: str
    algorithm: str
    email_token_expire_minutes: int = 10

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter='__')
    db: DBSettings
    smtp: SMTPSettings
    jwt: JWTSettings
    redis: RedisSettings
    api_prefix: str = '/api/v1'
    HOST: str
    PORT: int

    @property
    def BASE_URL(self) -> str:
        return f"http://{self.HOST}:{self.PORT}{self.api_prefix}"

settings = Settings(_env_file=BASE_DIR / '.env', _env_file_encoding='utf-8')

