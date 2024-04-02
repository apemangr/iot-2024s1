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


class Dispositivo:
    def __init__(self, linea):
        self.linea = linea.decode().strip()

    def obtener_tipo_dispositivo(self):
        tipo_dispositivo = "Device type: "
        if self.linea[3:5] == "01":
            tipo_dispositivo += "01 Temperatura, "
        else:
            tipo_dispositivo += "02 Humedad, "
        return tipo_dispositivo

    def obtener_id(self):
        return "ID: " + str(int(self.linea[6:8], 16))

    def obtener_datos(self):
        datos = ""
        if self.linea[3:5] == "01":
            datos += ", Temperatura relativa: " + str(int(self.linea[12:15], 16)) + "% "
        else:
            datos += ", Humedad relativa: " + str(int(self.linea[12:15], 16)) + "% "
        return datos

    def verificar_checksum(self):
        crc = crc16_ccitt_false_hex(self.linea[3:14].replace(" ", ""))
        if int(crc) == int(self.linea[15:20].replace(" ", ""), 16):
            return "Checksum: OK"
        else:
            return "Checksum: Wrong"

# Ejemplo de uso:
test_paquete = b'\x01\x01\x00\x07\xFF\xFF\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\xD0\xC5'
dispositivo = Dispositivo(test_paquete)
resultado = dispositivo.obtener_tipo_dispositivo() + dispositivo.obtener_id() + dispositivo.obtener_datos() + dispositivo.verificar_checksum()
print(resultado)
