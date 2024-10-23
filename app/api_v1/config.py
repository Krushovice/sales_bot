from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    BOT_TOKEN: str
    ECHO: bool = False
    TINKOFF_TERMINAL_KEY: str
    TINKOFF_PROD_TERMINAL_KEY: str
    TINKOFF_PROD_SECRET: str
    TINKOFF_SECRET: str
    OUTLINE_API_URL: str
    OUTLINE_SHA_CERT: str
    OUTLINE_USERS_GATEWAY: str
    ADMIN_ID: str
    ADVERTISER_ID: str
    EMAIL: str
    EMAIL_PSWD: str

    @property
    def db_url(self) -> str:
        return f"{self.DB_URL}"
        # return "sqlite+aiosqlite:///./db.sqlite3"

    @property
    def bot_token(self) -> str:
        return f"{self.BOT_TOKEN}"

    @property
    def get_tinkoff_token(self) -> str:
        return f"{self.TINKOFF_TOKEN}"

    @property
    def test_tinkoff_secret(self) -> str:
        return f"{self.TINKOFF_SECRET}"

    @property
    def test_tinkoff_terminal_key(self) -> str:
        return f"{self.TINKOFF_TERMINAL_KEY}"

    @property
    def tinkoff_secret(self) -> str:
        return f"{self.TINKOFF_PROD_SECRET}"

    @property
    def tinkoff_terminal_key(self) -> str:
        return f"{self.TINKOFF_PROD_TERMINAL_KEY}"

    @property
    def get_outline_url(self) -> str:
        return f"{self.OUTLINE_API_URL}"

    @property
    def get_outline_certificate(self) -> str:
        return f"{self.OUTLINE_SHA_CERT}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
