# Explicación del código de Fourier en Python

Este archivo contiene una clase en Python llamada **`Fourier`** que implementa dos algoritmos fundamentales en el análisis de señales:

- **Transformada Discreta de Fourier (TDF)**  
- **Transformada Rapida de Fourier (FFT)**  

La clase está diseñada para trabajar sin librerías externas como `numpy`, utilizando únicamente el módulo estándar `math`.

---

##  Estructura de la clase

### 1. `__init__(self, data)`
- **Entrada:**  
  - `data`: lista de valores reales o complejos que representan la señal.  
- **Proceso:**  
  - Convierte todos los valores a numeros complejos para asegurar compatibilidad.  
- **Salida:**  
  - Inicializa el objeto con la señal lista para transformarse.

---

### 2. `kernel(self, k, N)`
- **Entrada:**  
  - `k`: índice de frecuencia multiplicado por índice de tiempo.  
  - `N`: número total de muestras.  
- **Proceso:**  
  - Calcula el **kernel de Fourier**:  
    

\[
    e^{-2j \pi k / N}
    \]


- **Salida:**  
  - Devuelve un numero complejo que representa el peso de cada componente en la transformada.

---

### 3. `tdf(self)`
- **Entrada:**  
  - No recibe parametros adicionales (usa `self.data`).  
- **Proceso:**  
  - Implementa la **Transformada Discreta de Fourier** con doble bucle:  
    

\[
    X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-2j \pi kn / N}
    \]


- **Salida:**  
  - Lista de valores complejos que representan las frecuencias de la señal.

---

### 4. `_fft(self, x)`
- **Entrada:**  
  - `x`: sublista de datos en cada paso recursivo.  
- **Proceso:**  
  - Implementa el algoritmo recursivo de **Cooley–Tukey**:  
    - Divide la señal en indices pares e impares.  
    - Calcula la FFT de cada parte.  
    - Combina los resultados usando el kernel.  
- **Salida:**  
  - Lista de valores complejos transformados.

---

### 5. `fft(self)`
- **Entrada:**  
  - No recibe parametros adicionales (usa `self.data`).  
- **Proceso:**  
  - Llama a `_fft` para calcular la FFT completa.  
- **Salida:**  
  - Lista de valores complejos correspondientes a cada frecuencia.

---

### 6. `show_results(self, transform="fft")`
- **Entrada:**  
  - `transform`: puede ser `"tdf"` o `"fft"`.  
- **Proceso:**  
  - Ejecuta la transformada seleccionada.  
  - Imprime los resultados en consola mostrando parte real e imaginaria.  
- **Salida:**  
  - No retorna nada, solo imprime.

```python
import math

class Fourier:
    """
    Clase para calcular la Transformada Discreta de Fourier (TDF) y la
    Transformada Rápida de Fourier (FFT) de una señal.

    Parámetros
    ----------
    data : list[float | complex]
        Lista de valores reales o complejos que representan la señal de entrada.
    """

    def __init__(self, data: list[float | complex]) -> None:
        """
        Inicializa la clase con los datos de entrada.

        Parámetros
        ----------
        data : list[float | complex]
            Señal de entrada (lista de números).
        """
        self.data: list[complex] = [complex(x) for x in data]

    def kernel(self, k: int, N: int) -> complex:
        """
        Calcula el valor del kernel de Fourier.

        Fórmula: e^(-2j * pi * k / N)

        Parámetros
        ----------
        k : int
            Índice de frecuencia multiplicado por índice de tiempo.
        N : int
            Número total de muestras.

        Retorna
        -------
        complex
            Valor complejo del kernel.
        """
        return math.e ** (-2j * math.pi * k / N)

    def tdf(self) -> list[complex]:
        """
        Calcula la Transformada Discreta de Fourier (TDF).

        Retorna
        -------
        list[complex]
            Lista de valores complejos correspondientes a cada frecuencia.
        """
        N: int = len(self.data)
        result: list[complex] = []
        for k in range(N):
            suma: complex = 0j
            for n in range(N):
                suma += self.data[n] * self.kernel(k * n, N)
            result.append(suma)
        return result

    def _fft(self, x: list[complex]) -> list[complex]:
        """
        Algoritmo recursivo interno para calcular la FFT.

        Parámetros
        ----------
        x : list[complex]
            Sublista de datos en cada paso recursivo.

        Retorna
        -------
        list[complex]
            Lista de valores complejos transformados.
        """
        N: int = len(x)
        if N <= 1:
            return x
        even: list[complex] = self._fft(x[0::2])
        odd: list[complex] = self._fft(x[1::2])
        T: list[complex] = [self.kernel(k, N) * odd[k] for k in range(N // 2)]
        return [even[k] + T[k] for k in range(N // 2)] + \
               [even[k] - T[k] for k in range(N // 2)]

    def fft(self) -> list[complex]:
        """
        Calcula la Transformada Rápida de Fourier (FFT).

        Retorna
        -------
        list[complex]
            Lista de valores complejos correspondientes a cada frecuencia.
        """
        return self._fft(self.data)

    def show_results(self, transform: str = "fft") -> None:
        """
        Muestra los resultados de la transformada seleccionada.

        Parámetros
        ----------
        transform : str, opcional
            Tipo de transformada a mostrar: "tdf" o "fft".
            Por defecto es "fft".

        Retorna
        -------
        None
            Imprime los valores en consola.
        """
        if transform == "tdf":
            results: list[complex] = self.tdf()
            print("Resultados de la TDF:")
        else:
            results: list[complex] = self.fft()
            print("Resultados de la FFT:")

        for i, val in enumerate(results):
            print(f"Índice {i}: {val.real:.4f} + {val.imag:.4f}j")


# Ejemplo de uso
if __name__ == "__main__":
    datos: list[int] = [0, 1, 0, -1, 0, 1, 0, -1]
    f: Fourier = Fourier(datos)

    # Mostrar TDF
    f.show_results(transform="tdf")

    print("\n-----------------\n")

    # Mostrar FFT
    f.show_results(transform="fft")

```

