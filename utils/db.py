import psycopg2
import json


class Database():
    def __init__(self, databaseDict):
        self.host = databaseDict['host']
        self.username = databaseDict['username']
        self.password = databaseDict['password']
        self.port = databaseDict['port']
        self.dbname = databaseDict['database']
        self.connection = None

    def connect(self):
        if self.connection == None:
            try:
                self.connection = psycopg2.connect(host=self.host, user=self.username,password=self.password,port=self.port,dbname=self.dbname)
            except:
                print('Erro na conexão')
    
    
    def select_rows(self, query):
        self.connect()
        with self.connection.cursor() as cur:
            cur.execute(query)
            records = [row for row in cur.fetchall()]
            cur.close()
            return records
    
    def update_rows(self, query):
        self.connect()
        with self.connection.cursor() as cur:
            cur.execute(query)
            self.connection.commit()
            records = [row for row in cur.fetchall()]
            cur.close()
            return records