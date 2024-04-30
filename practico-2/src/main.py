from database.connection import * 
from service import Service
from entities.node import * 




servicio = Service(post)
temp = Temperature(False,20)
hum = Humidity(False,30)
node = NodeClass([hum],[temp],42)

