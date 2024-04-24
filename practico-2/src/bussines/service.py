from pandas.core.dtypes.dtypes import date
from ..database.connection import DbConnection
from ..entities.node import NodeClass

class Service:
    def __init__(self, db: DbConnection):
       self.db = db

    def createNode(self):
        try:
            cur = self.db.conn.cursor()
            cur.execute("SET TIMEZONE = 'America/Santiago'")
            cur.execute('INSERT INTO node_data(sampletime) SELECT CURRENT_TIME')
            self.db.conn.commit()
            return "Write successful"
        except:
            return "error in porcess of write"

    def createTemp(self,node: NodeClass):
        try: 
            cur = self.db.conn.cursor()
            for x in node.hum:
                cur.execute(f'INSERT INTO Humidity(node_id,humidity, alarm) VALUES({node.id},{x.hum},{x.alarm})')
                self.db.conn.commit()
            for x in node.tem:
                cur.execute(f'INSERT INTO Temperature(node_id,temperature, alarm) VALUES({node.id},{x.tem},{x.alarm})')
                self.db.conn.commit()
            return "Write successful"
        except:
            return "error in porcess of write"

    def remove(self,id: int):
       try: 
          cur = self.db.conn.cursor()
          cur.execute(F'DELETE FROM node_data WHERE id = {id}')
          self.db.conn.commit()
          return "Delete successful"
       except:
            return "error in porcess of Delete"

    def getOneById(self,id: int):
        return self.db.getQuery(F'SELECT * FROM node_data n INNER JOIN temperature t ON t.node_id = n.id INNER JOIN humidity h ON h.node_id = n.id WHERE n.id = {id} ')

    def getOneByHour(self,hrs: date):
        return self.db.getQuery(F'SELECT * FROM node_data n INNER JOIN temperature t ON t.node_id = n.id INNER JOIN humidity h ON h.node_id = n.id WHERE n.sample_time = {hrs} ')

    def getAllFromTemperature(self, temp: float):
        return self.db.getQuery(F'SELECT * FROM node_data n INNER JOIN temperature t ON t.node_id = n.id WHERE t.temperature = {temp} ')

    def getAllFromHumidity(self, hum: float):
        return self.db.getQuery(F'SELECT * FROM node_data n INNER JOIN humidity h ON h.node_id = n.id WHERE h.humidity = {hum} ')

    def getAll(self):
       return self.db.getQuery('SELECT * From node')



