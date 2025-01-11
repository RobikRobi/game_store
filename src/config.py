from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

class AuthData(BaseModel):
    private_key: Path = BASE_DIR /"src"/"auth"/"tokens"/"private_key.pem"
    public_key: Path = BASE_DIR /"src"/"auth"/"tokens"/"public_key.pem"
    algorithm: str = 'RS256'
    days: int = 31


configtoken = AuthData()

class Config(BaseSettings):
    database:str
    user: str
    password: str
    host: str
    class Config:
        env_file = ".env"

config = Config()