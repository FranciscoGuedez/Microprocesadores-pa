import math
import cmath

class FFTResponse:
    def __init__(
        self, valores: list, 
        magnitudes: list, 
        fases: list, 
        frecuencias: list
    ) -> None:
        self.valores = valores
        self.magnitudes = magnitudes
        self.fases = fases
        self.frecuencias = frecuencias
    
    def __repr__(self) -> dict[str,list]:
        return {
            "valores": self.valores,
            "magnitudes": self.magnitudes,
            "fases": self.fases,
            "frecuencias": self.frecuencias
        }