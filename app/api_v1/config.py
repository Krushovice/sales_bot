from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    BOT_TOKEN: str
    PAY_TOKEN: str
    DEBUG: bool = False
    ECHO: bool = True

    @property
    def db_url(self) -> str:
        if self.DEBUG:
            return "sqlite+aiosqlite:///./db.sqlite3"
        else:
            return f"{self.DB_URL}"

    @property
    def bot_token(self) -> str:
        return f"{self.BOT_TOKEN}"

    @property
    def pay_token(self) -> str:
        return f"{self.PAY_TOKEN}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
