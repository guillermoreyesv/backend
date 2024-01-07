from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os


class MySQLDBSingleton:
    _instance = None
    db: None
    session: None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MySQLDBSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance.db = None
            cls._instance.session = None
            cls._instance.connect_to_mysql()
        return cls._instance

    def connect_to_mysql(self):
        print('Starting connection')
        user = os.getenv('MYSQL_USER','admin')
        password = os.getenv('MYSQL_PASS','password')
        host = os.getenv('MYSQL_HOST','localhost')
        port = os.getenv('MYSQL_PORT','3306')
        dbname = os.getenv('DB_NAME','finvero')
        pool_recycle = os.getenv('DB_POOL_RECYCLE',3600)
        echo = os.getenv('DB_ECHO',False)
        
        uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}"
        self.db = create_engine(url=uri, pool_recycle=pool_recycle, echo=echo)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.db)

    def get_database(self):
        return self.db