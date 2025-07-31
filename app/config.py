import os
from dotenv import load_dotenv

load_dotenv()

# Naver Search OPEN API Keys
NAVER_CLIENT_ID: str = os.getenv("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET: str = os.getenv("NAVER_CLIENT_SECRET", "")

# NCP Keys
X_NCP_APIGW_API_KEY_ID: str = os.getenv("X_NCP_APIGW_API_KEY_ID", "")
X_NCP_APIGW_API_KEY: str = os.getenv("X_NCP_APIGW_API_KEY", "")

# MySQL 설정
MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "adkick_db")
MYSQL_USERNAME: str = os.getenv("MYSQL_USERNAME", "adkick_user")
MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
MYSQL_ROOT_PASSWORD: str = os.getenv("MYSQL_ROOT_PASSWORD", "")
MYSQL_BINDING_PORT: int = int(os.getenv("MYSQL_BINDING_PORT", "3306"))
MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_VOLUME: str = os.getenv("MYSQL_VOLUME", "./mysql_data")

REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
REDIS_BINDING_PORT: int = int(os.getenv("REDIS_BINDING_PORT", "6379"))
REDIS_DATA_PATH: str = os.getenv("REDIS_DATA_PATH", "./redis_data")
REDIS_DEFAULT_CONFIG_FILE: str = os.getenv("REDIS_DEFAULT_CONFIG_FILE", "redis.conf")
REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "1234")
REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
REDIS_MAX_CONNECTIONS: int = int(os.getenv("REDIS_MAX_CONNECTIONS", "10"))
REDIS_SOCKET_TIMEOUT: int = int(os.getenv("REDIS_SOCKET_TIMEOUT", "5"))
REDIS_CONNECT_TIMEOUT: int = int(os.getenv("REDIS_CONNECT_TIMEOUT", "5"))
REDIS_HEALTH_CHECK_INTERVAL: int = int(os.getenv("REDIS_HEALTH_CHECK_INTERVAL", "30"))

SECRET_KEY: str = os.getenv("SECRET_KEY")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
