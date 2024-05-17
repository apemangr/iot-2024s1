class Dispositivo:
    tipo=""
    datos=""
    alarm=True

    def __init__(self, linea):
        self.linea = linea

    @property
    def getTipoDispositivo(self):
        if self.linea[3:5] == "01":
            self.tipo += "Temperatura"
        else:
            self.tipo += "Humedad"
        return self.tipo

    @property
    def getDatos(self):
        self.dato =  int(self.linea[12:15], 16) 
        return self.dato

    @property
    def getAlarm(self):
        if self.linea == "01":
            if self.getDatos >= 100:
                self.alarm = True
            else:
                self.alarm = False
        else:
            if self.getDatos >= 20:
                self.alarm = True
            else:
                self.alarm = False
        return self.alarm




