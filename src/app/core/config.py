from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Email Service"
    RESEND_API_KEY: str
    API_KEY: str
    FROM_EMAIL: str
    FROM_EMAIL_NAME: str
    BASE_BACKEND_URL: str
    LOG_LEVEL: str = "INFO"

    TEMPLATE_FOLDER: str = "templates"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
