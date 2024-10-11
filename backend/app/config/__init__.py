from pydantic_settings import BaseSettings


# TODO: get variables from the environment!

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/application"
    project_name: str = "JobCrafter"
    version: str = "v0.0.0" # get version from pyproject.toml or use hardcoded...


settings = Settings()  # type: ignore
