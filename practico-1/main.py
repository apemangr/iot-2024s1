import serial

# Algoritmo "CRC-16/CCITT-False” 
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

resultado = ""

linea = puerto.readline().decode().strip()        


while True:
    linea = puerto.readline().decode().strip()        
    resultado += "Device type: "

    if linea[3:5] == "01":

        resultado += "01 Temperatura, "
    else:
        resultado += "02 Humedad, "

    # Tercer byte ID
    
    resultado += "ID: " +  str(int(linea[6:8], 16))

    # Cuarto byte Query (no se utiliza)

    # Quinto byte Datos
    if linea[3:5] == "01":
        resultado += ", Temperatura relativa: " + str(int(linea[12:15], 16)) + "% "
    else:
        resultado += ", Humedad relativa: " + str(int(linea[12:15], 16)) + "% "
 
    crc = crc16_ccitt_false_hex(linea[3:14].replace(" ", ""))

    if int(crc) == int(linea[15:20].replace(" ", ""), 16):
        resultado += "Checksum: OK"
    else:
        resultado += "Checksum: Wrong"
    
    print(resultado)
    resultado = ""

