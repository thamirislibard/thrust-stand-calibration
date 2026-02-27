import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# =====================================
# PARÂMETROS FÍSICOS DA BALANÇA
# =====================================

I = 0.025       # momento de inércia [kg.m²]
c = 0.002       # amortecimento viscoso [N.m.s/rad]
k = 1.5         # rigidez torsional [N.m/rad]
L = 0.3675      # braço da força [m]

omega_0 = np.sqrt(k / I)
zeta = c / (2 * np.sqrt(k * I))

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

def balanca_dinamica(t, x):
    theta, omega = x

    theta_dot = omega
    omega_dot = (L/I) * F(t) - (c/I) * omega - (k/I) * theta

    return [theta_dot, omega_dot]

# =====================================
# CONDIÇÕES INICIAIS
# =====================================

x0 = [0.0, 0.0]

# =====================================
# TEMPO DE SIMULAÇÃO
# =====================================

t0 = 0.0
tf = 50
t_eval = np.linspace(t0, tf, 6000)

# =====================================
# INTEGRAÇÃO
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
plt.xlabel("Tempo (s)")
plt.ylabel("Deflexão angular (µrad)")
plt.title("Resposta da balança a carregamento contínuo")
plt.grid()
plt.legend()

plt.show()
