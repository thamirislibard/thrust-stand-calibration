# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# 1. Configuração de Caminhos
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '..'))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from processing import apply_lowpass_filter

# 2. Constantes de Calibração
K_TORQUE = 0.0125
L_LVDT = 0.3
L_THRUST = 0.25
data_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'data.txt'))

def run_post_mission_analysis():
    if not os.path.exists(data_path):
        print("Erro: Arquivo data.txt não encontrado!")
        return

    # Gerar carimbo de tempo para o nome do arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Carregamento dos dados
    df = pd.read_csv(data_path, sep="\t", header=None, decimal=',')
    t = df[0].values
    d_raw = df[1].values * 1000 
    
    # Filtro de 0.1 Hz para estabilidade máxima no relatório
    d_filtered = apply_lowpass_filter(d_raw, fs=50, cutoff_freq=0.1)
    
    # Conversão para mN
    thrust = ((d_filtered / 1e6) / L_LVDT * K_TORQUE / L_THRUST) * 1000
    
    # Estatística dos últimos 5 segundos (regime permanente)
    steady_state = thrust[-250:] 
    avg_thrust = np.mean(steady_state)
    std_dev = np.std(steady_state)

    # Plotagem
    plt.figure(figsize=(12, 6))
    plt.plot(t, thrust, color='forestgreen', label='Sinal Processado (mN)')
    plt.axhline(y=avg_thrust, color='red', linestyle='--', 
                label=f'Empuxo Nominal: {avg_thrust:.4f} mN')
    
    plt.title(f"Relatório de Desempenho - Teste {timestamp}")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Empuxo (mN)")
    plt.grid(True, alpha=0.5)
    plt.legend()
    
    # Salva com nome único na pasta de resultados ou raiz
    output_name = f"resultado_{timestamp}.png"
    output_path = os.path.join(current_dir, '..', '..', output_name)
    plt.savefig(output_path)
    
    print(f"\n✅ Relatório gerado: {output_name}")
    print(f"📈 Empuxo Médio: {avg_thrust:.4f} mN")
    print(f"⚠️ Desvio Padrão: {std_dev:.6f} mN")

if __name__ == "__main__":
    run_post_mission_analysis()