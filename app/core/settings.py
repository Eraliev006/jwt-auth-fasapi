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

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter='__')
    db: DBSettings
    smtp: SMTPSettings
    api_prefix: str = '/api/v1'
    HOST: str
    PORT: int

settings = Settings(_env_file=BASE_DIR / '.env', _env_file_encoding='utf-8')

