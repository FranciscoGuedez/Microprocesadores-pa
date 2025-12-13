import math
import cmath

from fourier.core.fourier_response import FFTResponse
class Fourier:
    def __init__(self) -> None:
        pass

    def fft(self, x: list[complex]) -> list[complex]:
        """
        Implementación recursiva de la FFT (Cooley–Tukey).
        Se llama a sí misma.

        Parámetros:
            x : List[complex]  -> lista de muestras reales o complejas

        Retorna:
            List[complex]      -> coeficientes complejos de la FFT
        """
        N: int = len(x)

        # Caso base
        if N <= 1:
            return x

        # FFT recursiva en índices pares e impares
        X_even: list[complex] = self.fft(x[0::2])
        X_odd:  list[complex] = self.fft(x[1::2])

        # Factores twiddle
        T: list[complex] = [
            cmath.exp(-2j * math.pi * k / N) * X_odd[k]
            for k in range(N // 2)
        ]

        # Combinar resultados (butterfly)
        return (
            [X_even[k] + T[k] for k in range(N // 2)] +
            [X_even[k] - T[k] for k in range(N // 2)]
        )

    def mi_fft(self, x: list[float], fs: float = 1.0) -> FFTResponse:
        """
        Calcula FFT sin NumPy y devuelve todo tipado.

        Args:
            x  : List[float]  -> señal de entrada
            fs : float        -> frecuencia de muestreo

        Return:
            FFTResponse: respuesta formateada de componentes de fourier
        """

        N: int = len(x)

        # Convertir a complejos
        x_complex: list[complex] = [complex(v) for v in x]

        # 1. FFT
        valores_fft: list[complex] = self.fft(x_complex)

        # 2. Magnitudes
        magnitudes: list[float] = [abs(v) for v in valores_fft]

        # 3. Fases
        fases: list[float] = [cmath.phase(v) for v in valores_fft]

        # 4. Vector de frecuencias
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