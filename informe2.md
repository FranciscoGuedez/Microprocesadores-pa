# Implementación de la Transformada Discreta de Fourier (DFT) en Python

Este módulo define una clase llamada **`TransformadaDFT`**, que permite calcular la **Transformada Discreta de Fourier (DFT)** y su inversa (**IDFT**) de manera manual, sin depender de librerías externas como NumPy.  

---

##  Métodos principales

### `dft(x: List[float]) -> List[complex]`
- Recibe una lista de valores reales que representan una señal en el dominio del tiempo.
- Devuelve una lista de números complejos que corresponden a las frecuencias de la señal.
- Fórmula utilizada:



\[
X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j \cdot \frac{2\pi}{N} \cdot n \cdot k}
\]



---

### `idft(X: List[complex]) -> List[complex]`
- Recibe una lista de números complejos que representan la señal en el dominio de la frecuencia.
- Devuelve la reconstrucción de la señal en el dominio del tiempo.
- Fórmula utilizada:



\[
x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k] \cdot e^{j \cdot \frac{2\pi}{N} \cdot n \cdot k}
\]



---

##  Características del código
- Se emplea la librería **`cmath`** para manejar operaciones con números complejos.
- Se utiliza **`math.pi`** para calcular los ángulos de la transformada.
- El sistema de **logging** registra el proceso de análisis y facilita la depuración.
- La clase está pensada como un ejemplo educativo para comprender cómo funciona la DFT paso a paso.

---

##  Código en Python

```python
import logging
import cmath
import math
from typing import List

class TransformadaDFT:
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Inicializando analizador de Fourier...")

    def dft(self, x: List[float]) -> List[complex]:
        """
        Ejecuta una transformada discreta de Fourier.

        Args:
            x (List[float]): Números reales de la muestra de la señal.
        
        Returns:
            List[complex]: Lista de números complejos que representan la señal en frecuencia.
        """
        self.logger.info("Iniciando transformada de Fourier")
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

    def idft(self, X: List[complex]) -> List[complex]:
        """
        Ejecuta la transformada discreta inversa de Fourier.

        Args:
            X (List[complex]): Señal en el dominio de la frecuencia.
        
        Returns:
            List[complex]: Señal reconstruida en el dominio del tiempo.
        """
        N = len(X)
        x_rec = []
        for n in range(N):
            suma = 0
            for k in range(N):
                angulo = 2j * math.pi * n * k / N
                suma += X[k] * cmath.exp(angulo)
            x_rec.append(suma / N)
        return x_rec

        
```