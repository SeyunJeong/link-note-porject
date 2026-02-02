from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # OpenAI
    OPENAI_API_KEY: str = ""

    # App
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
