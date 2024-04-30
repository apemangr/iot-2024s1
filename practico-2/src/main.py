from database.connection import * 
from service import Service
from entities.node import * 
from other.extract_data import *
import serial

post.transaction("""CREATE TABLE IF NOT EXISTS node_data(
	                 id serial Primary Key,
	                 sampletime TIME
	                    )""")
                    
post.transaction("""CREATE TABLE IF NOT EXISTS temperature (
                     id serial Primary Key,
	                 node_data_id INTEGER NOT NULL,
	                 temperature DECIMAL(5,2),
	                 alarm BOOL,
	                 CONSTRAINT fk_node_data
	                 FOREIGN KEY (node_data_id)
	                 REFERENCES node_data (id)
	                 ON DELETE CASCADE
            	     ON UPDATE CASCADE
                    )""")
        
post.transaction("""CREATE TABLE IF NOT EXISTS humidity (
                     id serial Primary Key,
	                 node_data_id INTEGER NOT NULL,
	                 humidity DECIMAL(5,2),
	                 alarm BOOL,
	                 CONSTRAINT fk_node_data
	                 FOREIGN KEY (node_data_id)
	                 REFERENCES node_data (id)
	                 ON DELETE CASCADE
            	     ON UPDATE CASCADE
                    )""")

puerto = serial.Serial('/dev/ttyACM0', 57600, timeout=1)

servicio = Service(post)

hum = []
temp = []
id = 0
while True:
    buffer = 0
    servicio.createNode()
    id += 1
    while buffer <= 10:
        paquete = puerto.readline().decode().strip() 
        paquete = puerto.readline().decode().strip() 
        if paquete != '':
            buffer += 1
            dispositivo = Dispositivo(paquete)
            if dispositivo.getTipoDispositivo == 'Temperatura':
                t = Temperature(dispositivo.getAlarm,dispositivo.getDatos)
                temp.append(t)
            else:
                h = Humidity(dispositivo.getAlarm,dispositivo.getDatos)
                hum.append(h)
            print(dispositivo.getTipoDispositivo,dispositivo.getDatos,dispositivo.getAlarm)

    node = NodeClass(hum,temp,id)
    print(servicio.create(node))
    print(servicio.getAll())





