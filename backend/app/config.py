from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    data_dir: Path = Path("/app/data")
    secret_key: str = "change-me-in-production"
    debug: bool = False

    class Config:
        env_prefix = ""
        extra = "ignore"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_dir = Path(self.data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
