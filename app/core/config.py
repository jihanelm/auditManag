"""
from pydantic import BaseSettings

class Settings(BaseSettings):
    KEYCLOAK_URL: str = "http://localhost:8080"
    KEYCLOAK_REALM: str = "MyApp"
    KEYCLOAK_CLIENT_ID: str = "backend-app"
    KEYCLOAK_CERTS_URL: str = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"
    KEYCLOAK_TOKEN_URL: str = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"

    class Config:
        env_file = ".env"

settings = Settings()
"""