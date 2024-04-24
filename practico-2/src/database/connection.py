import psycopg2 as pg
import pandas as pd
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('.env'))

class DbConnection:
    def __init__(self,host,port,dbname,user,password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
    def __conn2db(self):
        try:
            self.connection = pg.connect(
                host = self.host,
                database = self.dbname,
                user = self.user,
                password = self.password
                    )
            return "Conexion exitosa"
        except:
            return "Fallo de conexion"

    @property
    def conn(self):
        self.__conn2db()
        return self.connection

    def getQuery(self, query):
        self.__conn2db()
        return pd.read_sql_query(query ,self.connection)

postgres = DbConnection(os.getenv('HOSTDB'),
                    os.getenv('PORTOUT'),
                    os.getenv('POSTGRES_DB'),
                    os.getenv('POSTGRES_USER'),
                    os.getenv('POSTGRES_PASSWORD'))

