"""
Settings

Para produccion, configure los siguientes secretos en Google Cloud Secret Manager:

- pjecz_portal_notarias_cloud_storage_deposito
- pjecz_portal_notarias_cloud_storage_deposito_edictos
- pjecz_portal_notarias_estado_clave
- pjecz_portal_notarias_host
- pjecz_portal_notarias_redis_url
- pjecz_portal_notarias_salt
- pjecz_portal_notarias_secret_key
- pjecz_portal_notarias_sqlalchemy_database_uri
- pjecz_portal_notarias_task_queue

Para desarrollo, debe crear un archivo .env con las variables de entorno:

- CLOUD_STORAGE_DEPOSITO
- CLOUD_STORAGE_DEPOSITO_EDICTOS
- ESTADO_CLAVE
- HOST
- REDIS_URL
- SALT
- SECRET_KEY
- SQLALCHEMY_DATABASE_URI
- TASK_QUEUE
"""

import os
from functools import lru_cache

from google.cloud import secretmanager
from pydantic_settings import BaseSettings

PROJECT_ID = os.getenv("PROJECT_ID", "")  # Por defecto esta vacio, esto significa estamos en modo local
SERVICE_PREFIX = os.getenv("SERVICE_PREFIX", "pjecz_portal_notarias")


def get_secret(secret_id: str) -> str:
    """Get secret from google cloud secret manager"""

    # If not in google cloud, return environment variable
    if PROJECT_ID == "":
        return os.getenv(secret_id.upper(), "")

    # Create the secret manager client
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    secret = f"{SERVICE_PREFIX}_{secret_id}"
    name = client.secret_version_path(PROJECT_ID, secret, "latest")

    # Access the secret version
    response = client.access_secret_version(name=name)

    # Return the decoded payload
    return response.payload.data.decode("UTF-8")


class Settings(BaseSettings):
    """Settings"""

    CLOUD_STORAGE_DEPOSITO: str = get_secret("cloud_storage_deposito")
    CLOUD_STORAGE_DEPOSITO_EDICTOS: str = get_secret("cloud_storage_deposito_edictos")
    HOST: str = get_secret("host")
    REDIS_URL: str = get_secret("redis_url")
    SALT: str = get_secret("salt")
    SECRET_KEY: str = get_secret("secret_key")
    SQLALCHEMY_DATABASE_URI: str = get_secret("sqlalchemy_database_uri")
    TASK_QUEUE: str = get_secret("task_queue")

    class Config:
        """Load configuration"""

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            """Customise sources, first environment variables, then .env file, then google cloud secret manager"""
            return env_settings, file_secret_settings, init_settings


@lru_cache()
def get_settings() -> Settings:
    """Get Settings"""
    return Settings()
