import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

#--------- DINAMICA DO PENDULO SIMPLES SEM AMORTECIMENTO ATIVO ---------#
#------- RESPOSTA AO IMPULSO DE FORÇA (DELTA DE DIRAC APROXIMADA) ---------#

# =====================================
# PARÂMETROS FÍSICOS DA BALANÇA
# =====================================
I = 0.025       # momento de inércia [kg.m²]
c = 0.002       # amortecimento viscoso [N.m.s/rad] 
k = 1.5         # rigidez torsional [N.m/rad]
L = 0.3675      # braço da força [m]

# Cálculo de propriedades dinâmicas
omega_0 = np.sqrt(k / I) 
zeta = c / (2 * np.sqrt(k * I))

print(f"ω₀ (Frequência Natural) = {omega_0:.4f} rad/s")
print(f"ζ  (Razão de Amortecimento) = {zeta:.4f}")

# =====================================
# DEFINIÇÃO DA FORÇA DE IMPULSO
# =====================================
def F(t):
    """
    Modelagem de um sinal de impulso (Delta de Dirac aproximada).
    O tau reduzido (0.0005) torna o sinal muito agudo, simulando um impacto.
    """
    J = 50e-6       #  Momento de impulso total (N.s) 
    tau = 0.0005    # Tempo característico de subida (quanto menor, mais agudo o impulso)
    t_impacto = 2 # Momento exato do impulso [s]

    # Função Gaussiana normalizada para que a integral seja sempre J
    return (J / (tau * np.sqrt(np.pi))) * np.exp(-(t - t_impacto)**2 / tau**2)

# =====================================
# SISTEMA DINÂMICO
# =====================================
def balanca_dinamica(t, x):
    theta, omega = x
    
    theta_dot = omega 
    # Equação: I*theta_dot + c*theta_dot + k*theta = L * F(t)
    omega_dot = (L/I) * F(t) - (c/I) * omega - (k/I) * theta

    return [theta_dot, omega_dot]

# =====================================
# CONFIGURAÇÃO DA SIMULAÇÃO
# =====================================
theta0 = 0.0      
omega0 = 0.0      
x0 = [theta0, omega0] # Condições iniciais: sem deflexão e sem velocidade

t0 = 0.0 
tf = 50 # Reduzi para 10s para ver melhor o início (ajuste se necessário)
t_eval = np.linspace(t0, tf, 10000) # Mais pontos para capturar a oscilação

# INTEGRAÇÃO NUMÉRICA
sol = solve_ivp( 
    balanca_dinamica,
    (t0, tf),
    x0,
    t_eval=t_eval, # Avaliação em pontos específicos para melhor resolução
    method='RK45', # Método de Runge-Kutta de ordem 5(4) para precisão
    rtol=1e-8, # Tolerância relativa mais rigorosa para capturar a resposta precisa
    atol=1e-10, # Tolerâncias mais rigorosas para capturar a resposta precisa
    max_step=0.001 # Passo máximo para garantir que o impulso seja bem resolvido
)

# Extração dos resultados
time = sol.t # Tempo de simulação
theta_urad = sol.y[0] * 1e6 # Convertendo para microrradianos

# =====================================
# PLOTS
# =====================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Gráfico da Força (Impulso)
ax1.plot(time, [F(ti) for ti in time], color='red', lw=1.5)
ax1.set_ylabel("Força de Impulso (N)")
ax1.set_title("Sinal de Entrada (Impulso Gaussiano Estreito)")
ax1.grid(True, alpha=0.3)

# Gráfico da Resposta Angular
ax2.plot(time, theta_urad, color='blue', lw=2, label="θ(t)")
ax2.set_xlabel("Tempo (s)")
ax2.set_ylabel("Deflexão (µrad)")
ax2.set_title("Resposta da Balança ao Impulso")
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()