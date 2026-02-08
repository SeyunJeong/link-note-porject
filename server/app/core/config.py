from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""

    # OpenAI
    OPENAI_API_KEY: str = ""

    # App
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
