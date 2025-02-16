import logging
import os
from dotenv import load_dotenv
load_dotenv()
FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(filename='userlogging.log',
                    level=logging.INFO, format=FORMAT)


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", None)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = Settings()
