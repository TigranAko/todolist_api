from pathlib import Path
from typing import Literal

from pydantic import SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

path_to_env = f"{Path().absolute().parent}/.env"


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=path_to_env,
        env_file_encoding="utf-8",
        extra="ignore",
    )


class ConfigDB(BaseConfig):
    ENVIROMENT: Literal["TEST", "DEV", "PROD"]
    TEST_DB_URL: SecretStr = "sqlite+aiosqlite:///:memory:"
    DEV_DB_URL: SecretStr = "sqlite+aiosqlite:///dev.db"
    PROD_DB_URL: SecretStr | None = None

    @computed_field
    def db_url(self) -> str:
        match self.ENVIROMENT:
            case "TEST":
                return self.TEST_DB_URL.get_secret_value()
            case "DEV":
                return self.DEV_DB_URL.get_secret_value()
            case "PROD":
                if self.PROD_DB_URL is None:
                    raise ValueError("Не удаось найти production базу данных")
                return self.PROD_DB_URL.get_secret_value()


config_db = ConfigDB()
# пример использлвания config_db.DB_URL.get_secret_value()
