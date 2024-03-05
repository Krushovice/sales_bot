from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    BOT_TOKEN: str
    PAY_TOKEN: str
    DEBUG: bool = False
    ECHO: bool = False
    YOOKASSA_APP_ID: str
    YOOKASSA_ACCESS_TOKEN: str
    YOOKASSA_CLIENT_SECRET: str
    OUTLINE_API_URL: str
    OUTLINE_SHA_CERT: str

    @property
    def db_url(self) -> str:
        # if self.DEBUG:
        #     return "sqlite+aiosqlite:///./db.sqlite3"
        # else:
        return f"{self.DB_URL}"

    @property
    def bot_token(self) -> str:
        return f"{self.BOT_TOKEN}"

    @property
    def pay_token(self) -> str:
        return f"{self.PAY_TOKEN}"

    @property
    def get_app_id(self) -> str:
        return f"{self.YOOKASSA_APP_ID}"

    @property
    def get_yookassa_token(self) -> str:
        return f"{self.YOOKASSA_ACCESS_TOKEN}"

    @property
    def get_pay_secret(self) -> str:
        return f"{self.YOOKASSA_CLIENT_SECRET}"

    @property
    def get_outline_url(self) -> str:
        return f"{self.OUTLINE_API_URL}"

    @property
    def get_outline_certificate(self) -> str:
        return f"{self.OUTLINE_SHA_CERT}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
