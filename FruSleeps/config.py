import os
from dotenv import load_dotenv

load_dotenv()
#if not os.getenv("POSTGRESQL_ADDON_URI"):
#    raise RuntimeError("DATABASE_URL is not set")

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #load_dotenv()
    #if not os.getenv("POSTGRESQL_ADDON_URI"):
    #    raise RuntimeError("DATABASE_URL is not set")
    URI = os.getenv("POSTGRESQL_ADDON_URI")
    DEBUG=False
    DEVELOPMENT=False
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    load_dotenv()
    #if not os.getenv("POSTGRESQL_ADDON_URI"):
    #    raise RuntimeError("DATABASE_URL is not set")
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = os.getenv("POSTGRESQL_ADDON_URI")
    SECRET_KEY=os.getenv("SECRET_KEY")

class TestingConfig(Config):
   DEBUG = True
   TESTING = True
   SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")


config = {
   'development': DevelopmentConfig,
   'testing': TestingConfig,
   'default': DevelopmentConfig}   