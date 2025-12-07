# Informe sobre los codigos en 

### Clase Anapu (listar puertos disponibles)

**Explicación:**  
### La clase `Anapu` sirve para obtener los puertos seriales activos en el sistema.  El método `listar_puertos_activos()` usa `serial.tools.list_ports.comports()` para devolver una lista de puertos disponibles (ejemplo: `COM3` en Windows o `/dev/ttyUSB0` en Linux).

```python
import serial
import serial.tools.list_ports

class Anapu:
    def init(self):
        pass

    def listar_puertos_activos(self) -> list:
        puertos = serial.tools.list_ports.comports()
        return puertos

```

### Clase Signal (lectura y graficado de señales)

**Explicación:**  
### La clase `Signal` se encarga de abrir un puerto serial, leer datos enviados por un dispositivo (por ejemplo, una Raspberry Pi) y graficarlos en tiempo real.  
- En el constructor (`init`) se configuran el puerto y la velocidad de transmisión (`baudrate`) y se abre la conexión serial con `Serial()`.  
- `leer_linea()`: lee una línea completa desde el puerto serial, la decodifica en UTF-8 y elimina espacios en blanco.  
- `leer_valores()`: interpreta la línea recibida si está en formato de lista (ejemplo: `[1.2, 2.3, 3.1]`), separa los valores y los convierte a números flotantes.  
- `stream()`: activa el modo interactivo de matplotlib y en un bucle infinito va leyendo valores, limpiando la gráfica y dibujando los puntos. Se fija un rango de voltaje entre 0 y 3.3 V y se actualiza la gráfica en tiempo real.

```python
from serial import Serial
import matplotlib.pyplot as plt

class Signal:
    def init(self, baudrate: int = 115200, port: str = "COM3"):
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


```


### Probar puertos disponibles

**Explicación:**  
Este fragmento de código importa la clase `Anapu` desde el módulo `app.puertos`.  
- Se crea un objeto `Anapu`.  
- Se llama al método `listar_puertos_activos()` para obtener la lista de puertos seriales disponibles en el sistema.  
- Luego se recorre esa lista con un bucle `for` y se imprime cada puerto encontrado en la consola.  
Esto sirve para verificar qué dispositivos están conectados y en qué puerto se encuentran.

```python
from app.puertos import Anapu

puertos = Anapu()
puertos_disponibles = puertos.listar_puertos_activos()
for p in puertos_disponibles:
    print(p)

```

### Probar la señal

**Explicación:**  
Este fragmento de código combina el uso de la clase `Anapu` y la clase `Signal`.  
- Primero se instancia `Anapu` para listar los puertos seriales disponibles en el sistema y se imprimen en consola.  
- Luego se crea un objeto `Signal` indicando el puerto `COM3` como destino de la conexión serial.  
- Se llama al método `leer_valores()` para obtener una lista de valores enviados por el dispositivo conectado.  
- Se imprimen esos valores en consola.  
- Finalmente, se ejecuta `signal.stream()` que abre una ventana de matplotlib y grafica los valores en tiempo real, mostrando el voltaje de la señal recibida.

```python
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

```

### Clase TransformadaDFT (DFT e IDFT)

**Explicación:**  
La clase `TransformadaDFT` implementa la **Transformada Discreta de Fourier (DFT)** y su inversa (**IDFT**).  
- En el constructor (`init`) se inicializa un logger para registrar mensajes de depuración.  
- `dft(x)`: recibe una lista de números reales (la señal en el dominio del tiempo) y calcula sus componentes de frecuencia. Para cada frecuencia `k`, suma todas las muestras multiplicadas por el factor exponencial `exp(-2jπnk/N)`. El resultado es una lista de números complejos que representan el espectro de la señal.  
- `idft(X)`: recibe una lista de coeficientes complejos (espectro) y reconstruye la señal original en el dominio del tiempo. Para cada muestra `n`, suma todos los coeficientes multiplicados por el factor `exp(2jπnk/N)` y divide entre `N`. El resultado es la señal reconstruida.

```python
import logging
import cmath
import math
from typing import List

class TransformadaDFT:
    def init(self):
        self.logger = logging.getLogger(f'[{self.class.name}]')
        self.logger.info("Inicializando analizador de Fourier...")

    def dft(self, x: List[float]) -> List[complex]:
        N = len(x)
        X = []
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

```

### Clase Fourier (FFT)

**Explicación:**  
La clase `Fourier` implementa la **Transformada Rápida de Fourier (FFT)** mediante el algoritmo recursivo de Cooley–Tukey.  
- En el constructor (`init`) no se inicializa nada, pero está definido para futuras extensiones.  
- `fft(x)`: recibe una lista de números complejos y calcula la FFT.  
  - Si la longitud de la lista es 1, devuelve directamente el valor (caso base).  
  - Divide la señal en índices pares e impares, calcula la FFT de cada parte recursivamente y luego combina los resultados usando los factores twiddle `exp(-2jπk/N)`.  
  - El resultado es una lista de coeficientes complejos que representan el espectro de la señal.  
- `mi_fft(x, fs)`: recibe una lista de valores reales (la señal en el tiempo) y la frecuencia de muestreo `fs`.  
  - Convierte la señal a complejos.  
  - Calcula la FFT usando el método anterior.  
  - Obtiene las magnitudes (amplitud de cada frecuencia) y las fases (ángulo de cada componente).  
  - Construye el vector de frecuencias, con valores positivos y negativos según el índice.  
  - Devuelve un objeto `FFTResponse` que encapsula todos los resultados: coeficientes, magnitudes, fases y frecuencias.

```python
import math
import cmath
from fourier.core.fourier_response import FFTResponse

class Fourier:
    def init(self) -> None:
        pass

    def fft(self, x: list[complex]) -> list[complex]:
        N: int = len(x)
        if N <= 1:
            return x
        X_even: list[complex] = self.fft(x[0::2])
        X_odd:  list[complex] = self.fft(x[1::2])
        T: list[complex] = [
            cmath.exp(-2j * math.pi * k / N) * X_odd[k]
            for k in range(N // 2)
        ]
        return (
            [X_even[k] + T[k] for k in range(N // 2)] +
            [X_even[k] - T[k] for k in range(N // 2)]
        )

    def mi_fft(self, x: list[float], fs: float = 1.0) -> FFTResponse:
        N: int = len(x)
        x_complex: list[complex] = [complex(v) for v in x]
        valores_fft: list[complex] = self.fft(x_complex)
        magnitudes: list[float] = [abs(v) for v in valores_fft]
        fases: list[float] = [cmath.phase(v) for v in valores_fft]
        freqs: list[float] = []
        for k in range(N):
            if k < N // 2:
                freqs.append(k * fs / N)
            else:
                freqs.append((k - N) * fs / N)
        result = FFTResponse(
            valores=valores_fft,
            magnitudes=magnitudes,
            fases=fases,
            frecuencias=freqs
        )
        return result

```

### Clase Fourier (FFT y análisis de señal)

**Explicación:**  
La clase `Fourier` implementa la **Transformada Rápida de Fourier (FFT)** mediante el algoritmo recursivo de Cooley–Tukey y además ofrece un método para calcular la FFT de una señal real con frecuencia de muestreo.  
- En el constructor (`init`) no se inicializa nada, pero está definido para futuras extensiones.  
- `fft(x)`: recibe una lista de números complejos y calcula la FFT.  
  - Si la longitud de la lista es 1, devuelve directamente el valor (caso base).  
  - Divide la señal en índices pares e impares, calcula la FFT de cada parte recursivamente y luego combina los resultados usando los factores twiddle `exp(-2jπk/N)`.  
  - El resultado es una lista de coeficientes complejos que representan el espectro de la señal.  
- `mi_fft(x, fs)`: recibe una lista de valores reales (la señal en el tiempo) y la frecuencia de muestreo `fs`.  
  - Convierte la señal a complejos.  
  - Calcula la FFT usando el método anterior.  
  - Obtiene las magnitudes (amplitud de cada frecuencia) y las fases (ángulo de cada componente).  
  - Construye el vector de frecuencias, con valores positivos y negativos según el índice.  
  - Devuelve un objeto `FFTResponse` que encapsula todos los resultados: coeficientes, magnitudes, fases y frecuencias.

```python
import math
import cmath
from fourier.core.fourier_response import FFTResponse

class Fourier:
    def init(self) -> None:
        pass

    def fft(self, x: list[complex]) -> list[complex]:
        N: int = len(x)
        if N <= 1:
            return x
        X_even: list[complex] = self.fft(x[0::2])
        X_odd:  list[complex] = self.fft(x[1::2])
        T: list[complex] = [
            cmath.exp(-2j * math.pi * k / N) * X_odd[k]
            for k in range(N // 2)
        ]
        return (
            [X_even[k] + T[k] for k in range(N // 2)] +
            [X_even[k] - T[k] for k in range(N // 2)]
        )

    def mi_fft(self, x: list[float], fs: float = 1.0) -> FFTResponse:
        N: int = len(x)
        x_complex: list[complex] = [complex(v) for v in x]
        valores_fft: list[complex] = self.fft(x_complex)
        magnitudes: list[float] = [abs(v) for v in valores_fft]
        fases: list[float] = [cmath.phase(v) for v in valores_fft]
        freqs: list[float] = []
        for k in range(N):
            if k < N // 2:
                freqs.append(k * fs / N)
            else:
                freqs.append((k - N) * fs / N)
        result = FFTResponse(
            valores=valores_fft,
            magnitudes=magnitudes,
            fases=fases,
            frecuencias=freqs
        )
        return result

```