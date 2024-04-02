import serial

def crc16_ccitt_false_hex(data_hex):
    # Convertir la cadena hexadecimal en una secuencia de bytes
    data_bytes = bytes.fromhex(data_hex)
    
    crc = 0xFFFF
    
    for byte in data_bytes:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    
    return crc

puerto = serial.Serial('COM3', 9600, timeout=1)

class Dispositivo:
    tipo=""
    id=""
    checksum=""
    datos=""
    def __init__(self, linea):
        self.linea = linea

    def __setTipoDispositivo(self):
        if self.linea[3:5] == "01":
            self.tipo += "01 Temperatura"
        else:
            self.tipo += "02 Humedad"
        return self.tipo

    def __setId(self):
        self.id = str(int(self.linea[6:8], 16))
        return self.id

    def __setChecksum(self):
        crc = crc16_ccitt_false_hex(self.linea[3:14].replace(" ", ""))
        if int(crc) == int(self.linea[15:20].replace(" ", ""), 16):
           self.checksum = "Checksum: OK"
        else:
            self.checksum = "Checksum: Wrong"
        return self.checksum

    def __obtener_datos(self):
        if self.linea[3:5] == "01":
            self.dato =  str(int(self.linea[12:15], 16)) + "%"
        else:
            self.dato =  str(int(self.linea[12:15], 16)) + "%"
        return self.dato

    def getData(self):
        print('Device type: ', self.__setTipoDispositivo(), ", ID: ", self.__setId(),", Temperatura relativa: ",self.__obtener_datos(),", ",self.__setChecksum())

# Ejemplo de uso:
paquete = puerto.readline().decode().strip() 
paquete = puerto.readline().decode().strip() 
dispositivo = Dispositivo(paquete)
dispositivo.getData()

