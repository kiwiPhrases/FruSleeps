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
    RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")
    RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
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
    RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")
    RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
    SECRET_KEY=os.getenv("SECRET_KEY")

class TestingConfig(Config):
   DEBUG = True
   TESTING = True
   RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")
   RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
   SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")


config = {
   'development': DevelopmentConfig,
   'testing': TestingConfig,
   'default': DevelopmentConfig}   