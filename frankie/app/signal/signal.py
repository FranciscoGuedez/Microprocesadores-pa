from serial import Serial
import matplotlib.pyplot as plt

class Signal:
    def __init__(self, baudrate: int = 115200, port: str = "COM3"):
        self.baudrate = baudrate
        self.port = port
        self.ser = Serial(self.port, self.baudrate, timeout=1)
    
    def leer_linea(self) -> str:
        lectura = self.ser.readline()
        return lectura.decode("utf-8").strip()
    
    def leer_valores(self) -> list[float]:
        linea = self.leer_linea()
        if linea.startswith("[") and linea.endswith("]"):
            valores = linea[1:-1].split(",")
            response = [float(v.strip()) for v in valores]
            return response
        return []
    
    def stream(self):
        plt.ion()
        fig, ax = plt.subplots()

        while True:
            valores = self.leer_valores()
            if valores:
                ax.clear()
                ax.plot(valores, marker='o')
                ax.set_ylim(0, 3.3)
                ax.set_title('Raspberry')
                ax.set_xlabel('Muestra')
                ax.set_ylabel('Voltaje')
                plt.pause(0.01)