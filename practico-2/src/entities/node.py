from .humidity import *
from .temperature import *

class NodeClass: 
    def __init__(self, hum: list[Humidity], tem: list[Temperature],id: int):
        self.hum = hum
        self.tem = tem
        self.id = id

