from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

path_to_env = f"{Path.absolute().parent}/.env"


class BaseConfig(BaseSettings):
    model_confifg = SettingsConfigDict(
        env_file=path_to_env,
        env_file_encoding="utf-8",
        extra="ignore",
    )
