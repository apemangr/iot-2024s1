from .humidity import *
from .temperature import *

class NodeClass: 
    def __int__(self,hum: list[Humidity], tem: list[Temperature],id):
        self.hum = hum
        self.tem = tem
        self.id = id

