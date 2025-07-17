from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Pydantic settings class to manage environment variables.
    """
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
