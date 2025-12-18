from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ===== CORE APP =====
    APP_NAME: str = "Shift Bot"
    DEBUG: bool = False

    # ===== DATABASE =====
    DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"
        extra = "allow"  # umožní ATT_* a jiné modulární promìnné


settings = Settings()
