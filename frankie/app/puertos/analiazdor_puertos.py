import serial
import serial.tools.list_ports

class Anapu:
    def __init__(self):
        pass

    def listar_puertos_activos(self) -> list:
        puertos = serial.tools.list_ports.comports()
        return puertos