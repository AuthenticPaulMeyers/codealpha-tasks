import os
from dotenv import load_dotenv

load_dotenv(override=True)

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

def get_config(env):
    return {
        "development": DevelopmentConfig,
        "production": ProductionConfig
    }.get(env, DevelopmentConfig)
