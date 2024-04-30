from database.connection import * 
from service import Service
from entities.node import * 
from other.extract_data import *
from serial import Serial

#NOTE: construccion de tablas en caso de no estar creadas.
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

#NOTE: Puerto serial de lectura de datos.
puerto = Serial('/dev/ttyACM0', 57600, timeout=1)

#NOTE: Inicializacion de servicios CRUD.
servicio = Service(post)

#NOTE: datos de entrada de base de datos
hum = []
temp = []
id = 0

#NOTE: Bucle de recoleccion de datos de sensores
while True:
    hum = []
    temp = []
    buffer = 0           #NOTE:<-- setea bufer en 0
    servicio.createNode()#NOTE:<-- creacion de nodo padre en base de datos
    id += 1              #NOTE:<-- id nodo creado

    #NOTE: Recoleccion de 12 datos de humdad y temperatura, en un periodo de tiempo
    while buffer <= 12:
        paquete = puerto.readline().decode().strip() 
        paquete = puerto.readline().decode().strip() 
        if paquete != '':
            buffer += 1
            dispositivo = Dispositivo(paquete)
            #NOTE: lista de objetos y datos recolectados para posterior almacenamiento
            if dispositivo.getTipoDispositivo == 'Temperatura':
                t = Temperature(dispositivo.getAlarm,dispositivo.getDatos)
                temp.append(t)                                            
            else:
                h = Humidity(dispositivo.getAlarm,dispositivo.getDatos)
                hum.append(h)
            print(dispositivo.getTipoDispositivo,dispositivo.getDatos,dispositivo.getAlarm)

    #NOTE: Almacenamiento de datos creados con su respectivo nodo padre
    node = NodeClass(hum,temp,id)
    print(servicio.create(node))
    print(servicio.getAll())





