import numpy as np
from scipy import signal

def apply_lowpass_filter(data, fs=100, cutoff_freq=0.3, order=5):
    """
    Aplica um filtro Butterworth de 5ª ordem com fase zero (filtfilt).
    Garante que o sinal fique limpo sem atrasar o tempo dos picos.
    """
    # Proteção: scipy exige um número mínimo de pontos para filtrar
    if len(data) < 30:
        return data
        
    nyquist = 0.5 * fs
    normal_cutoff = cutoff_freq / nyquist
    
    # Geração dos coeficientes do filtro
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    
    # Filtragem bidirecional para fase zero
    return signal.filtfilt(b, a, data)

def convert_to_mn(displacement_um, k_torque, l_thrust, l_lvdt):
    """
    Converte o deslocamento lido (em micrômetros) para Força (mN).
    Fórmula baseada na mecânica da balança de torção.
    """
    # 1. Converter micrômetros para metros
    displacement_m = displacement_um / 1_000_000.0
    
    # 2. Calcular o ângulo de deflexão (radianos)
    # tan(theta) approx theta para pequenos ângulos
    theta = displacement_m / l_lvdt
    
    # 3. Calcular o Torque (N.m)
    torque = k_torque * theta
    
    # 4. Calcular o Empuxo (Newtons)
    thrust_n = torque / l_thrust
    
    # 5. Retornar em Milli-Newtons (mN)
    return thrust_n * 1000

def calculate_metrics(time, thrust_mn):
    """
    Extrai métricas estatísticas para o relatório final.
    Calcula o Bias (erro de zero) e o Empuxo Nominal.
    """
    # O Bias é calculado nos primeiros segundos (antes do motor ligar)
    bias = np.mean(thrust_mn[:50]) if len(thrust_mn) > 50 else 0
    
    # O Empuxo Nominal é a média do platô (pico) menos o bias
    thrust_puro = thrust_mn - bias
    nominal_thrust = np.max(thrust_puro)
    
    return {
        "bias": bias,
        "nominal_thrust": nominal_thrust,
        "peak_value": np.max(thrust_mn)
    }