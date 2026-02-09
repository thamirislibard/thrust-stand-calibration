import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.processing import apply_lowpass_filter, convert_to_mn, calculate_metrics
import io

st.set_page_config(page_title="Thrust Stand Control - IAC 2026", layout="wide")
plt.style.use('dark_background')

st.title("🚀 Sistema de Aquisição e Processamento de Dados")

# --- BARRA LATERAL: CONFIGURAÇÕES ---
with st.sidebar:
    st.header("⚙️ Parâmetros de Calibração")
    k_torque = st.number_input("Constante K (N.m/rad)", value=0.1500, format="%.4f")
    l_thrust = st.number_input("Braço do Motor (m)", value=0.100, format="%.3f")
    l_lvdt = st.number_input("Braço do Sensor (m)", value=0.120, format="%.3f")
    
    st.markdown("---")
    st.subheader("🧪 Ambiente de Teste")
    btn_simular = st.button("📊 Gerar Ensaio Simulado")
    
    st.markdown("---")
    st.subheader("🔌 Configuração de Hardware")
    porta_com = st.text_input("Porta COM (ex: COM3)", "COM3")
    st.caption("Ajuste a porta conforme reconhecido no Windows.")

# --- FUNÇÃO DE PROCESSAMENTO CENTRALIZADA ---
def rodar_analise(df):
    try:
        # Conversão forçada para garantir que 'str' vire 'float' 
        raw_data = df['raw_disp'].values.astype(float)
        time_data = df['time'].values.astype(float)
        
        # Backend Processing
        filtered = apply_lowpass_filter(raw_data)
        thrust_mn = convert_to_mn(filtered, k_torque, l_thrust, l_lvdt)
        metrics = calculate_metrics(time_data, thrust_mn)

        # 1. Cards de Resultados Rápidos
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Empuxo Nominal", f"{metrics['nominal_thrust']:.4f} mN")
        col2.metric("Bias (Referência)", f"{metrics['bias']:.4f} mN")
        col3.metric("Pico Máximo", f"{metrics['peak_value']:.4f} mN")
        col4.metric("Ruído RMS (STD)", f"{np.std(thrust_mn):.4f} mN")

        # 2. Gráfico do Ensaio
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(time_data, thrust_mn, color='#2ecc71', label='Sinal Processado (mN)', linewidth=1.2)
        ax.axhline(y=metrics['bias'], color='#e74c3c', linestyle='--', label='Nível de Bias')
        ax.set_title("Comportamento do Empuxo na Bancada", fontsize=12)
        ax.set_xlabel("Tempo (s)")
        ax.set_ylabel("Força (mN)")
        ax.grid(True, alpha=0.2)
        ax.legend()
        st.pyplot(fig)

        # 3. Gerador de Relatórios (Downloads)
        st.markdown("### 📄 Gerador de Laudos e Exportação")
        c_down1, c_down2 = st.columns(2)
        
        # Exportar planilha
        df_proc = pd.DataFrame({'Tempo (s)': time_data, 'Empuxo (mN)': thrust_mn})
        csv = df_proc.to_csv(index=False).encode('utf-8')
        c_down1.download_button("📥 Baixar Dados Processados (.csv)", data=csv, file_name="ensaio_iac_2026.csv")
        
        # Exportar gráfico para o artigo
        img = io.BytesIO()
        fig.savefig(img, format='png', dpi=300)
        c_down2.download_button("🖼️ Baixar Gráfico para o Artigo (.png)", data=img, file_name="grafico_ensaio.png")

        # 4. Tabela de Análise Estatística
        st.markdown("### 📊 Estatísticas Detalhadas")
        stats_df = pd.DataFrame({
            "Métrica": ["Média Aritmética", "Desvio Padrão", "Variância do Sinal", "Valor Mínimo", "Pico Máximo"],
            "Valor (mN)": [np.mean(thrust_mn), np.std(thrust_mn), np.var(thrust_mn), np.min(thrust_mn), np.max(thrust_mn)]
        })
        st.table(stats_df)

    except Exception as e:
        st.error(f"Erro no processamento: {e}")

# --- CORPO PRINCIPAL (ABAS) ---
tab1, tab2 = st.tabs(["📊 Relatórios e Análise", "📡 Telemetria Real-Time"])

with tab1:
    if btn_simular:
        st.subheader("🔍 Resultados do Ensaio Simulado")
        t = np.linspace(0, 10, 1000)
        # Cria sinal de 50mN com ruído gaussiano
        sinal_sim = np.where((t > 2) & (t < 8), 50, 0) + np.random.normal(0, 5, 1000)
        df_sim = pd.DataFrame({'time': t, 'raw_disp': sinal_sim})
        rodar_analise(df_sim)
    
    else:
        st.subheader("Gerador de Relatórios e Análise Estatística")
        up_file = st.file_uploader("Carregar Log de Teste (.txt)", type=['txt'])
        
        if up_file:
            # Ajustado para ler o seu data.txt com espaços e vírgulas
            df_real = pd.read_csv(
                up_file, 
                sep=r'\s+', 
                names=['time', 'raw_disp'], 
                decimal=',', 
                engine='python'
            )
            
            if st.button("🎯 Processar Dados e Gerar Gráfico"):
                rodar_analise(df_real)

with tab2:
    st.subheader("🔌 Conexão com a Bancada de Testes")
    
    c_inst, c_status = st.columns([2, 1])
    
    with c_inst:
        st.markdown(f"""
        ### Como conectar o Hardware:
        1. **Cabo USB:** Conecte o sensor ao computador.
        2. **Porta Serial:** Verifique se a porta é a **{porta_com}**.
        3. **Leitura:** Clique no botão abaixo para iniciar o fluxo.
        """)
        
        if st.button("🚀 Estabelecer Conexão USB"):
            st.toast("Iniciando driver serial...", icon="🔌")
            st.info(f"Escutando porta {porta_com}... Aguardando dados do LVDT.")
    
    with c_status:
        st.success("✅ Interface Pronta")
        st.write("**Status:** Aguardando comando")

    st.divider()
    st.markdown("### 📈 Monitoramento em Tempo Real")
    # Placeholder para o gráfico dinâmico
    fig_live, ax_live = plt.subplots(figsize=(10, 3))
    ax_live.set_title("Fluxo de Dados: Hardware Desconectado")
    st.pyplot(fig_live)