from pathlib import Path
from typing_extensions import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "apps" / "certs" / "private_key.pem"
    public_key_path: Path = BASE_DIR / "apps" / "certs" / "public_key.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 150
    refresh_token_expire_minutes: int = 60 * 24 * 30


class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    MODE: Literal["DEV", "PROD", "TEST"] = "DEV"

    DB_USER: str
    DB_PASS: str
    DB_PORT: int
    DB_HOST: str
    DB_NAME: str

    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_PORT: int
    TEST_DB_HOST: str
    TEST_DB_NAME: str

    API_KEY_KINOPOISK: str

    AUTH_JWT: AuthJWT = AuthJWT()

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://\
{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def TEST_DB_URL(self):
        return f"postgresql+asyncpg://\
{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"


settings = Setting()  # type: ignore
