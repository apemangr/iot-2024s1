from pandas.core.dtypes.dtypes import date
from database.connection import DbConnection
from entities.node import NodeClass

class Service:
    def __init__(self, db: DbConnection):
       self.db = db

    def createNode(self):
        self.db.transaction("INSERT INTO node_data(sampletime) VALUES (CURRENT_TIMESTAMP)")

    def create(self,node: NodeClass):
        try: 
            for x in node.hum:
                self.db.transaction(str(f'INSERT INTO humidity(node_data_id,humidity, alarm) VALUES({node.id},{x.hum},{x.alarm})'))
            for x in node.tem:
                self.db.transaction(str(f'INSERT INTO temperature(node_data_id,temperature, alarm) VALUES({node.id},{x.tem},{x.alarm})'))
            return "Write successful"
        except:
            return "error in porcess of write"

    def remove(self,id: int):
       try: 
          self.db.transaction(F'DELETE FROM node_data WHERE id = {id}')
          return "Delete successful"
       except:
            return "error in porcess of Delete"

    def getOneById(self,id: int):
        return self.db.getQuery(str(F'SELECT * FROM node_data n INNER JOIN temperature t ON t.node_data_id = n.id INNER JOIN humidity h ON h.node_data_id = n.id WHERE n.id = {id}'))

    def getOneByHour(self,hrs: date):
        return self.db.getQuery(F'SELECT * FROM node_data n INNER JOIN temperature t ON t.node_data_id = n.id INNER JOIN humidity h ON h.node_data_id = n.id WHERE n.sample_time = {hrs} ')

    def getAllFromTemperature(self, temp: float):
        return self.db.getQuery(F'SELECT * FROM node_data n INNER JOIN temperature t ON t.node_data_id = n.id WHERE t.temperature = {temp} ')

    def getAllFromHumidity(self, hum: float):
        return self.db.getQuery(str(F'SELECT * FROM node_data n INNER JOIN humidity h ON h.node_data_id = n.id WHERE h.humidity = {hum}'))

    def getAll(self):
       return self.db.getQuery(str('SELECT * From node_data'))



