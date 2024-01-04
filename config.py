import os
from dotenv import load_dotenv



class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    load_dotenv()
    if not os.getenv("POSTGRESQL_ADDON_URI"):
        raise RuntimeError("DATABASE_URL is not set")
    URI = os.getenv("POSTGRESQL_ADDON_URI")
   
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    load_dotenv()
    if not os.getenv("POSTGRESQL_ADDON_URI"):
        raise RuntimeError("DATABASE_URL is not set")
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = os.getenv("POSTGRESQL_ADDON_URI")

class TestingConfig(Config):
   DEBUG = True
   TESTING = True
   SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")


config = {
   'development': DevelopmentConfig,
   'testing': TestingConfig,
   'default': DevelopmentConfig}   