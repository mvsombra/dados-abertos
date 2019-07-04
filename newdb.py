import sqlalchemy as sql
import os


class Database:
    def __init__(self):
        self.engine = sql.create_engine(os.environ['DATABASE_URL'])
        self.conn = self.engine.connect()
