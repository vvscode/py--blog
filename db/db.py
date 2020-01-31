import os
from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
    os.path.join(basedir, "blog.db")

engine = create_engine(SQLALCHEMY_DATABASE_URI)
