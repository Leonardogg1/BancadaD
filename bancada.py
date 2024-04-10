import serial
import numpy as np
from scipy.fft import fft
from simple_pid import PID

# Configuração do Serial
ser = serial.Serial('COM8', 9600)  # Substitua 'COM3' pela porta onde o Arduino está conectado
s = ser.read()
# Configuração do PID
pid = PID(1.0, 0.1, 0.05, setpoint=1)
pid.output_limits = (0, 255)  # Assume que o controle é feito com um valor de 8 bits

def find_main_freq(signal):
    # Aplicando FFT ao sinal
    N = len(signal)
    T = 1.0 / 800.0  # Supondo uma taxa de amostragem de 800 Hz
    yf = fft(signal)
    print(yf)
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    idx_max = np.argmax(np.abs(yf[0:N//2]))
    return xf[idx_max]

while True:
    line = ser.readline()  # Lê uma linha do serial
    #print(line)
    try:
        # Convertendo a linha de entrada em uma lista de inteiros
        values = list(map(int, line.decode('utf-8').strip().split(',')))
        print(values)
        if len(values) == 4:  # Certifica-se de que há 4 valores
            main_freq = find_main_freq(values)
            #print("{:.10f}".format(main_freq))
            control_signal = pid(main_freq)
            print(control_signal)
            # Envia o sinal de controle de volta para o Arduino
            ser.write(str(control_signal).encode())
    except ValueError:
        # Acontece se a conversão falhar
        print("Erro na leitura dos dados.")
