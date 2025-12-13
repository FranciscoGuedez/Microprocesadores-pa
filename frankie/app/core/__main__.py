import math
import logging
from fourier.core import TransformadaDFT
from fourier.core import Fourier

if __name__ == "__main__":
    transformada = Fourier()

    fs = 100  # frecuencia de muestreo
    N = 32    # muestras

    t = [n / fs for n in range(N)]
    x = [2 * math.sin(2 * math.pi * 5 * ti) for ti in t]

    resultado = transformada.mi_fft(x, fs)

    valores = resultado.valores
    i = 0
    for valor in valores:
        print(f"Resultado {i} es: {valor}")
        i = i + 1


    logging.basicConfig(level="INFO")

    t = TransformadaDFT()
    x = [1, 2, 3, 4]

    print("DFT:", t.dft(x))
    #print("IDFT:", t.idft(t.dft(x)))