from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/application"
    test: bool = False
    project_name: str = "JobCrafter"


settings = Settings()  # type: ignore
