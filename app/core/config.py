import os

from dotenv import load_dotenv

load_dotenv()
#postgresql://postgres:y1Hr19R00wolYA1FUTVoul-bbUiEFPnE@postgres.railway.internal:5432/

#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:12345678@localhost:5432/water_bender")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:y1Hr19R00wolYA1FUTVoul-bbUiEFPnE@turntable.proxy.rlwy.net:32243/railway")
SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
N8N_WEBHOOK_URL = os.getenv(
    "N8N_WEBHOOK_URL",
    "https://primary-production-b9528.up.railway.app/webhook/chat",
)
