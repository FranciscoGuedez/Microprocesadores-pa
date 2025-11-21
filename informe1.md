# Generación de PWM en Raspberry Pi Pico

Este programa utiliza el módulo machine de MicroPython para generar una señal **PWM (Pulse Width Modulation)** en el pin GPIO 15 de la Raspberry Pi Pico, con una frecuencia fija de **5 kHz**.

## Funcionamiento
- Se configura el pin 15 como salida PWM.
- La señal varía su **ciclo de trabajo (duty cycle)** desde 0 hasta 100% y luego desciende nuevamente.
- En cada paso se calculan parámetros eléctricos importantes:
  - **Vp (Voltaje pico):** igual al voltaje de alimentación del GPIO (3.3 V).
  - **Vpp (Voltaje pico a pico):** también 3.3 V.
  - **Vavg (Voltaje promedio):** proporcional al ciclo de trabajo.
  - **Vrms (Voltaje eficaz):** depende de la raíz cuadrada del duty cycle.
  - **f (frecuencia):** constante en 5 kHz.
  - **T (período):** inverso de la frecuencia, 200 µs.

## Detalles adicionales
- El rango del duty cycle en MicroPython va de **0 a 65535**, lo que representa la resolución de 16 bits del PWM.
- El cálculo de **Vavg** y **Vrms** permite entender cómo se comporta la señal en términos de energía entregada a una carga resistiva.
- El retardo de time.sleep(0.1) asegura que los cambios en el ciclo de trabajo sean visibles y no demasiado rápidos.
- El bucle principal alterna entre una **rampa ascendente** y una **rampa descendente**, generando un efecto de variación continua en la señal.

## Observaciones
- Aunque el voltaje máximo del GPIO es fijo (3.3 V), el **valor promedio y eficaz** dependen directamente del duty cycle.
- Este tipo de cálculos son útiles para analizar cómo una señal PWM puede simular diferentes niveles de voltaje en sistemas digitales.
- El código imprime en consola los valores calculados en cada iteración, lo que facilita la comprensión del comportamiento eléctrico de la señal.


``` python 
from machine import Pin, PWM
import time, math

# Configuración PWM
pwm = PWM(Pin(15))
pwm.freq(5000)   # Frecuencia fija de 5 kHz
Vcc = 3.3        # Voltaje de salida del Pico (GPIO)

while True:
    for duty in range(0, 65535, 5000):  # Subida
        pwm.duty_u16(duty)
        duty_ratio = duty / 65535  # Duty normalizado (0 a 1)

        # Cálculos eléctricos
        Vp = Vcc
        Vpp = Vcc
        Vavg = duty_ratio * Vcc
        Vrms = math.sqrt(duty_ratio) * Vcc
        f = 5000
        T = 1 / f

        print(f"Duty={duty_ratio:.2f} | Vp={Vp:.2f} V | Vpp={Vpp:.2f} V | Vavg={Vavg:.2f} V | Vrms={Vrms:.2f} V | f={f} Hz | T={T*1e6:.1f} us")
        time.sleep(0.1)

    for duty in range(65535, 0, -5000):  # Bajada
        pwm.duty_u16(duty)
        duty_ratio = duty / 65535

        Vp = Vcc
        Vpp = Vcc
        Vavg = duty_ratio * Vcc
        Vrms = math.sqrt(duty_ratio) * Vcc
        f = 5000
        T = 1 / f

        print(f"Duty={duty_ratio:.2f} | Vp={Vp:.2f} V | Vpp={Vpp:.2f} V | Vavg={Vavg:.2f} V | Vrms={Vrms:.2f} V | f={f} Hz | T={T*1e6:.1f} us")
        time.sleep(0.1)
```