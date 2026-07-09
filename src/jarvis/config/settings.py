from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Jarvis"
    app_version: str = "0.1.0"

    groq_api_key: str
    
    tavily_api_key: str

    default_model: str = "qwen/qwen3-32b"

    llm_provider: str = "groq"
    
    log_level: str = "INFO"

    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()