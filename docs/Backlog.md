# Backlog - Thrust Balance Calibration - LaSE

Este documento serve como backlog do repositório do projeto **Thrust Balance Calibration - LaSE**, contendo as principais tarefas, requisitos e prioridades. Para detalhes adicionais, consulte a [planilha de acompanhamento no Google Sheets](https://docs.google.com/spreadsheets/d/1bI2x75SJOgQma6dlL40EmWFeJrbb3BSSk1ROJQhcD8Q/edit?usp=sharing).

---

## 📌 Visão Geral do Projeto
**Objetivo**:  
Desenvolver um sistema de calibração de balança de empuxo (thrust balance) para aplicações no Laboratório de Sistemas Espaciais (LaSE).

**Principais Entregas**:
- Software de aquisição e processamento de dados.
- Documentação técnica e relatórios de calibração.
- Interface de usuário para configuração e monitoramento.

---

## 📋 Backlog de Tarefas

### 🚀 Tarefas Prioritárias
1. **Definição de Requisitos**
   - [x] Levantamento de requisitos com a equipe do LaSE.
   - [ ] Documentação de especificações técnicas.

2. **Desenvolvimento do Software**
   - [ ] Implementação da aquisição de dados via sensores.
   - [ ] Criação de algoritmos de calibração.
   - [ ] Desenvolvimento da interface gráfica.

3. **Testes e Validação**
   - [ ] Testes em bancada com carga conhecida.
   - [ ] Validação dos resultados com a equipe.

4. **Documentação**
   - [ ] Manual de usuário.
   - [ ] Relatório técnico de calibração.

---

### 🔗 Links Úteis
- [📊 Planilha de Acompanhamento no Google Sheets](https://docs.google.com/spreadsheets/d/1bI2x75SJOgQma6dlL40EmWFeJrbb3BSSk1ROJQhcD8Q/edit?usp=sharing)  
  *(Acesse para detalhes sobre prazos, responsáveis, status das tarefas, lista de materiais e referências)*

- [📂 Repositório do Projeto](https://github.com/thamirislibard/tcc-thrust_balance.git)  
  *(Código-fonte e documentação técnica)*

---

## 🗓️ Próximos Passos
- [ ] Montagem do **sistema de posicionamento** do LVDT.
- [ ] **Calibração com pesos** da balança.
    - [ ] Padronizar contra-pesos.
    - [ ] Posicionar corretamente o LVDT.
    - [ ] Gráficos de comportamento do sensor com diferentes pesos aplicados.
    - [ ] Fazer breve manual de aplicação - pesos utilizados, tamanho do contra-peso, códigos utilizados para gerar resultados.
    - **Sempre fazer anotações do que for conduzido!**
- [ ] Calibração eletromagnética.
    - Modelagem 3D dos componentes.
        - [x] Suporte eletroímã, suporte ímã permanente em ABS para testes.
        - [ ] Suporte eletroímã, suporte ímã permanente em resina.
    - [ ] Projetar detalhadamente o sistema.
    - [ ] Fazer análise da tensão aplicada no eletrímã para a força de repulsão/atração (não são iguais. Os testes devem ser conduzidos igualmente para ambos os casos) com uma distância x entre eles (a distância pode e deve ser alterada. Os testes devem ser conduzidos igualmente para cada distância. Anotações, sempre.).
    - [ ] Código.

---

**Atualizado em**: 22/05/2025 
**Responsável**: Thamiris Libard


## 💻 Guia de Execução e Operação (Software)
```
python -m venv .venv

.\.venv\Scripts\activate

pip install -r requirements.txt
```

### **🚀 Como Executar o Sistema**
Para rodar o software localmente, é necessário garantir que o ambiente virtual esteja ativo:

1. **Ativar o Ambiente Virtual (venv):**
   - No Windows: `.\venv\Scripts\activate`
   - No Linux/Mac: `source venv/bin/activate`
2. **Iniciar a Interface:**
   - No terminal, execute: `streamlit run main.py`
3. O sistema abrirá automaticamente no navegador no endereço `localhost:8501`.

### **🎮 Operação da Interface**
* **Configuração Técnica (Sidebar):** Ajuste em tempo real da **Constante K** e dos **Braços de Alavanca ($L$)**.
* **Módulo de Análise (Aba 1):** * **Ensaio Simulado:** Gera dados sintéticos com ruído para validar o filtro e a calibração sem hardware.
    * **Processamento de Logs:** Suporte para arquivos `data.txt` com separadores decimais de vírgula (`,`) e colunas por espaço.
* **Telemetria Real-Time (Aba 2):** Guia para conexão USB, identificação de porta Serial e monitoramento de fluxo bruto.
* **Exportação:** Botões para baixar **gráficos (PNG)** e **planilhas processadas (CSV)** com métricas de Média, Pico e RMS.