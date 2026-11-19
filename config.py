from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    db_host:str
    db_port:int
    db_user:str
    db_password:str
    db_name:str
    JWT_SECRET_KEY:str
    JWT_ALGORITHM: str="HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES:int=30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int=7

    model_config=SettingsConfigDict(env_file=".env",
                                    env_file_encoding="utf-8",
                                    case_sensitive=False,
                                    extra="ignore"
        )
settings=Settings()