

from b24demo1.configs import BaseConfig as config

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(config.SQLALCHEMY_DATABASE_URI,encoding='utf-8', echo=False)
db = scoped_session(sessionmaker(autocommit=False,autoflush=False, bind=engine))