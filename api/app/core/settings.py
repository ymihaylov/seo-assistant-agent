from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    auth0_domain: str
    auth0_audience: str

    openai_api_key: str
    openai_model: str
    openai_base_url: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @property
    def issuer(self) -> str:
        return f"https://{self.auth0_domain}/"


def get_settings() -> Settings:
    return Settings()
