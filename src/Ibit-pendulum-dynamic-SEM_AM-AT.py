import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

#--------- DINAMICA DO PENDULO SIMPLES SEM AMORTECIMENTO ATIVO ---------#

# =====================================
# PARÂMETROS FÍSICOS DA BALANÇA
# =====================================

I = 0.025       # momento de inércia [kg.m²] CORRIGIR
c = 0.002       # amortecimento viscoso [N.m.s/rad] VALOR APROXIMADO/CORRIGIR PARA MELHOR PRECISÃO
k = 1.5         # rigidez torsional [N.m/rad] CORRIGIR/APROXIMADO
L = 0.3675        # braço da força [m] OK


omega_0 = np.sqrt(k / I) # Frequência natural
zeta = c / (2 * np.sqrt(k * I)) # Razão de amortecimento

print(f"ω₀ = {omega_0:.4f} rad/s")
print(f"ζ  = {zeta:.4f}")


# =====================================
# DEFINIÇÃO DA FORÇA F(t)
# =====================================

def F(t):
    """
    Força aplicada pelo thruster [N]
    """
    J = 50e-6       # impulso total [N.s] (50 µNs)
    tau = 0.002     # duração característica do pulso [s]

    return (J / (tau * np.sqrt(np.pi))) * np.exp(-(t - 0.05)**2 / tau**2)


# =====================================
# SISTEMA DINÂMICO (1ª ORDEM)
# =====================================

def balanca_dinamica(t, x):
    theta, omega = x

    theta_dot = omega
    omega_dot = (L/I) * F(t) - (c/I) * omega - (k/I) * theta

    return [theta_dot, omega_dot]


# =====================================
# CONDIÇÕES INICIAIS
# =====================================

theta0 = 0.0      # rad
omega0 = 0.0      # rad/s
x0 = [theta0, omega0]


# =====================================
# TEMPO DE SIMULAÇÃO
# =====================================

t0 = 0.0
tf = 50

t_eval = np.linspace(t0, tf, 5000)


# =====================================
# INTEGRAÇÃO NUMÉRICA
# =====================================

sol = solve_ivp(
    balanca_dinamica,
    (t0, tf),
    x0,
    t_eval=t_eval,
    method='RK45',
    rtol=1e-8,
    atol=1e-10
)

theta = sol.y[0]
omega = sol.y[1]
time = sol.t


# =====================================
# PLOTS
# =====================================

plt.figure(figsize=(10,6))

plt.plot(time, theta * 1e6, lw=2, label="θ(t)")

plt.xlabel("Tempo (s)", fontsize=12)
plt.ylabel("Deflexão angular (µrad)", fontsize=12)
plt.title("Resposta dinâmica da balança ao impulso", fontsize=14)
plt.grid()
plt.legend()

plt.show()
