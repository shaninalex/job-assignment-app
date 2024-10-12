from pydantic_settings import BaseSettings


# TODO: get variables from the environment!


class Settings(BaseSettings):
    project_name: str = "JobCrafter"
    version: str = "v0.0.0"  # TODO: get version from pyproject.toml or use hardcoded...
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/application"
    secret: str = "<app secret from environment>"



settings = Settings()  # type: ignore
