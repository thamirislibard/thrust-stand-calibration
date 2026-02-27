import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# =====================================
# PARÂMETROS FÍSICOS DA BALANÇA
# =====================================

I = 0.025       # momento de inércia [kg.m²] - Resistência do sistema à aceleração angular.
c = 0.0002       # coeficiente de amortecimento viscoso [N.m.s/rad] - Dissipação de energia por viscosidade.
k = 1.5         # rigidez torsional [N.m/rad] - Constante de mola angular do fio de suspensão.
L = 0.3675      # braço da força [m] - Distância do eixo à aplicação da força.

print("Iniciando.")

omega_0 = np.sqrt(k / I)  # frequência natural do sistema (sem amortecimento) [rad/s] - A frequência na qual o sistema oscilaria se não houvesse amortecimento.
zeta = c / (2 * np.sqrt(k * I)) # fator de amortecimento adimensional - Indica o tipo de resposta do sistema (subamortecido, criticamente amortecido ou superamortecido).

print(f"ω₀ = {omega_0:.4f} rad/s")
print(f"ζ  = {zeta:.4f}")

# =====================================
# DEFINIÇÃO DA FORÇA CONTÍNUA
# =====================================

def F(t):
    F0 = 50e-6   # força constante [N]
    tau = 0.02   # tempo característico de subida [s]

    return F0 * (1 - np.exp(-t / tau))

# =====================================
# SISTEMA DINÂMICO
# =====================================

def balanca_dinamica(t, x): # tempo e vetor de estado 
    theta, omega = x # vetor de estado: deflexão angular e velocidade angular

    theta_dot = omega # a variação da posição no tempo é igual à velocidade angular
    # omega_dot é a aceleração angular, que é determinada pela soma dos torques aplicados ao sistema, dividida pelo momento de inércia.

    omega_dot = (L/I) * F(t) - (c/I) * omega - (k/I) * theta
    # Termos da equação de movimento:
    # (L/I) . F(t): O torque causado por uma força externa aplicada a uma distância L.
    # -(c/I) . omega: A força de amortecimento (atrito), que se opõe ao movimento.
    # -(k/I) . theta: A força de restauração (mola), que tenta trazer a balança de volta ao centro.

    return [theta_dot, omega_dot]

# =====================================
# CONDIÇÕES INICIAIS
# =====================================

x0 = [0.0, 0.0] # vetor de estado inicial: [deflexão angular, velocidade angular] - A balança começa em repouso, sem deflexão e sem movimento angular.

# =====================================
# TEMPO DE SIMULAÇÃO
# =====================================

t0 = 0.0 # tempo inicial [s]
tf = 50 # duração total da simulação [s]
t_eval = np.linspace(t0, tf, 6000) # pontos de avaliação para obter uma resolução temporal adequada, especialmente para capturar a resposta inicial do sistema.

# =====================================
# INTEGRAÇÃO
# =====================================

# A função solve_ivp é utilizada para resolver o sistema de equações diferenciais. 
# O método 'RK45' é um método de Runge-Kutta de ordem 5(4) que é eficiente para resolver problemas de valor inicial. 
# Os parâmetros rtol e atol são definidos para garantir uma alta precisão na solução, especialmente importante para capturar a resposta inicial do sistema.

sol = solve_ivp(
    balanca_dinamica, # função que define o sistema dinâmico
    (t0, tf),
    x0,
    t_eval=t_eval,
    method='RK45',
    rtol=1e-8,
    atol=1e-10
)

theta = sol.y[0] # deflexão angular [rad] - A resposta do sistema à força aplicada ao longo do tempo.
omega = sol.y[1] # velocidade angular [rad/s] - A taxa de variação da deflexão angular, que também é afetada pela força aplicada e pelas características do sistema (inércia, amortecimento e rigidez).
time = sol.t # vetor de tempo correspondente às soluções obtidas para theta e omega, utilizado para plotar a resposta do sistema ao longo do tempo.

# =====================================
# PLOTS
# =====================================

plt.figure(figsize=(10,6))

plt.plot(time, theta * 1e6, lw=2, label="θ(t)")
plt.xlabel("Tempo (s)")
plt.ylabel("Deflexão angular (µrad)")
plt.title("Resposta da balança a carregamento contínuo")
plt.grid()
plt.legend()

plt.show()

print("Simulação concluída.")
