import logging
import cmath
import math
from typing import List

class TransformadaDFT:
    """
    Loremp ipsum
    """
    def __init__(self):
        self.logger = logging.getLogger(f'[{self.__class__.__name__}]')
        self.logger.info("Inicializando analizador de Fourier...")

    def dft(self, x: List[float]) -> List[complex]:
        """
        Ejecuta una transformada discret de Fourier

        Args:
            x(List): Numeros reales de la muestra de la senal
        
        Returns:
            List[complex]: Lista de numeros complejos
        """
        self.logger.info("Iniciando transformada de fourier")
        N = len(x)
        X = []
        self.logger.info(f"Analizando {N} muestras")
        for k in range(N):
            suma = 0
            for n in range(N):
                angulo = -2j * math.pi * n * k / N
                suma += x[n] * cmath.exp(angulo)
            X.append(suma)
        return X

    def idft(self, X):
        N = len(X)
        x_rec = []
        for n in range(N):
            suma = 0
            for k in range(N):
                angulo = 2j * math.pi * n * k / N
                suma += X[k] * cmath.exp(angulo)
            x_rec.append(suma / N)
        return x_rec
