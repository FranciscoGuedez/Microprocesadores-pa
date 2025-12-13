from app.puertos import Anapu

puertos = Anapu()
puertos_disponibles = puertos.listar_puertos_activos()
for p in puertos_disponibles:
    print(p)