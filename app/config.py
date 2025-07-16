import os
from dotenv import load_dotenv

load_dotenv()

# Naver Search OPEN API Keys
NAVER_CLIENT_ID: str = os.getenv("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET: str = os.getenv("NAVER_CLIENT_SECRET", "")

# NCP Keys
X_NCP_APIGW_API_KEY_ID: str = os.getenv("X_NCP_APIGW_API_KEY_ID", "")
X_NCP_APIGW_API_KEY: str = os.getenv("X_NCP_APIGW_API_KEY", "")