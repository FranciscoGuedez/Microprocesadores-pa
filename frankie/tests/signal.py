from app.signal import Signal
from app.puertos import Anapu

puertos = Anapu()
disponibles = puertos.listar_puertos_activos()
for puerto in disponibles:
    print(puerto)

signal = Signal(port='COM3')
valores = signal.leer_valores()
print(valores)
signal.stream()