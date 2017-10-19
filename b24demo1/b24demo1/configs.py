import logging

class BaseConfig(object):
    VS_DEBUG = False
    DEBUG = False
    SECRET_KEY = 'b24demo1_secret_key'

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:Youra070213470@localhost:5432/b24demo1'

    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'app.log'
    LOGGING_LEVEL = logging.INFO

class DevelopmentConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass