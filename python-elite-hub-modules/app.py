from modules.suitability import SuitabilityEngine
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Importação dos módulos personalizados
# Certifique-se de que a pasta /modules existe com os arquivos correspondentes
from modules.calculators import WealthCalculator
from modules.news_engine import NewsEngine

# --- 1. CONFIGURAÇÃO DE INTERFACE (ESTILO BLOOMBERG) ---
st.set_page_config(page_title="Elite Financial Hub", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 8px; }
    div[data-testid="stMetricValue"] { color: #00ff41; font-family: 'Courier New', monospace; }
    .news-card { padding: 15px; border-bottom: 1px solid #30363d; background-color: #161b22; margin-bottom: 10px; border-radius: 4px; }
    .news-title { color: #58a6ff; font-weight: bold; text-decoration: none; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NAVEGAÇÃO LATERAL ---
with st.sidebar:
    st.title("🏛️ Elite Hub")
    st.subheader("Wealth Management")
    st.markdown("---")
    
    menu = st.radio(
    "Navegação Estratégica",
    ["📊 Diagnóstico Patrimonial", "📈 Calculadora de Juros", "📟 Terminal de Notícias", "🎯 Perfil de Risco", "👤 Meu Perfil"]
)
    
    st.markdown("---")
    st.caption(f"Status: Conectado\nData: {datetime.now().strftime('%d/%m/%Y')}")
    st.caption("Especialista: Fernando Cláudio")

# --- 3. LÓGICA DAS PÁGINAS ---

# --- PÁGINA: DIAGNÓSTICO PATRIMONIAL ---
if menu == "📊 Diagnóstico Patrimonial":
    st.title("📊 Diagnóstico de Eficiência Patrimonial")
    st.write("Analise a saúde do seu fluxo de caixa e o impacto da inflação.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        receita = st.number_input("Receita Mensal Líquida", value=25000.0, step=1000.0)
        despesa = st.number_input("Despesa Mensal Média", value=15000.0, step=1000.0)
    with c2:
        patrimonio_atual = st.number_input("Patrimônio Investido", value=300000.0, step=10000.0)
        ipca_est = st.slider("Expectativa IPCA (% a.a.)", 2.0, 12.0, 4.5) / 100
    with c3:
        st.write("### Alpha Real")
        excedente = receita - despesa
        savings_rate = (excedente / receita) if receita > 0 else 0
        st.metric("Capacidade de Aporte", f"R$ {excedente:,.2f}")
        st.metric("Savings Rate", f"{savings_rate:.1%}")

    if st.button("GERAR INSIGHT ESTRATÉGICO"):
        perda_ipca = patrimonio_atual * ipca_est
        st.error(f"🛡️ **Alerta de Erosão:** Sem alocação correta, seu patrimônio perderá R$ {perda_ipca:,.2f} de poder de compra em 12 meses.")
        
        # Gráfico de impacto simples
        fig, ax = plt.subplots(figsize=(8, 2))
        fig.patch.set_facecolor('#0d1117')
        ax.set_facecolor('#0d1117')
        ax.barh(['Poder de Compra'], [patrimonio_atual], color='#30363d')
        ax.barh(['Poder de Compra'], [patrimonio_atual - perda_ipca], color='#00ff41')
        ax.tick_params(colors='white')
        st.pyplot(fig)

# --- PÁGINA: CALCULADORA DE JUROS ---
elif menu == "📈 Calculadora de Juros":
    st.title("📈 Engenharia de Juros Compostos")
    
    with st.container():
        col_in, col_res = st.columns([1, 2])
        
        with col_in:
            st.write("### Parâmetros")
            p_ini = st.number_input("Capital Inicial", value=300000.0)
            p_aport = st.number_input("Aporte Mensal", value=5000.0)
            p_anos = st.slider("Prazo (Anos)", 1, 30, 10)
            p_taxa = st.slider("Taxa Estimada (% a.a.)", 5.0, 20.0, 11.25) / 100
            p_inf = st.slider("Inflação (IPCA) (% a.a.)", 2.0, 10.0, 4.5) / 100

        # Chamada da lógica do módulo calculators.py
        df_res = WealthCalculator.juros_compostos_avancado(p_ini, p_aport, p_taxa, p_anos, p_inf)
        
        with col_res:
            st.write("### Evolução Patrimonial")
            st.area_chart(df_res.set_index("Mês")[["Saldo Nominal (R$)", "Total Aportado (R$)"]])
            
            m_final = df_res["Saldo Nominal (R$)"].iloc[-1]
            m_real = df_res["Poder de Compra (R$)"].iloc[-1]
            
            k1, k2 = st.columns(2)
            k1.metric("Montante Final (Nominal)", f"R$ {m_final:,.2f}")
            k2.metric("Poder Real (Valor de Hoje)", f"R$ {m_real:,.2f}")

# --- PÁGINA: TERMINAL DE NOTÍCIAS ---
elif menu == "📟 Terminal de Notícias":
    st.title("📟 Market Intelligence Terminal")
    st.write("Pulso do mercado em tempo real com análise de sentimento via IA.")
    
    if st.button("ATUALIZAR TERMINAL"):
        st.cache_data.clear()

    engine = NewsEngine()
    with st.spinner("Conectando às fontes financeiras..."):
        df_news = engine.fetch()
        
        if not df_news.empty:
            for _, row in df_news.iterrows():
                st.markdown(f"""
                    <div class="news-card">
                        <span style="font-size: 0.8rem; color: #8b949e;">{row['source']} | {row['sentiment']}</span><br>
                        <a class="news-title" href="{row['link']}" target="_blank">{row['title']}</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Nenhuma notícia capturada no momento.")

# --- PÁGINA: PERFIL DE RISCO (SUITABILITY) ---
if menu == "🎯 Perfil de Risco":
    st.header("🎯 Análise de Perfil de Investidor (Suitability)")
    st.write("Identifique a alocação ideal com base no seu horizonte e tolerância a risco.")
    
    with st.form("suitability_form"):
        q1 = st.selectbox("Qual o seu objetivo principal?", 
                          options=[(2, "Preservar Capital"), (4, "Aumentar Patrimônio"), (6, "Máxima Rentabilidade")])
        q2 = st.selectbox("Por quanto tempo pretende manter os investimentos?", 
                          options=[(2, "Curto Prazo (< 1 ano)"), (4, "Médio Prazo (1-5 anos)"), (6, "Longo Prazo (> 5 anos)")])
        q3 = st.selectbox("Qual sua reação a uma queda de 10% na carteira?", 
                          options=[(2, "Resgataria tudo"), (4, "Manteria e aguardaria"), (6, "Aproveitaria para aportar mais")])
        
        btn_perfil = st.form_submit_button("GERAR PERFIL TÉCNICO")
    
    if btn_perfil:
        # Extrai os pontos das tuplas selecionadas
        pontos = [q1[0], q2[0], q3[0]]
        resultado = SuitabilityEngine.calcular_perfil(pontos)
        
        st.markdown(f"### Seu Perfil: <span style='color:{resultado['cor']}'>{resultado['perfil']}</span>", unsafe_allow_html=True)
        st.info(f"**Sugestão de Alocação:** {resultado['alocacao']}")

# --- PÁGINA: PERFIL ---
elif menu == "👤 Meu Perfil":
    st.title("👤 Consultoria de Investimentos de Elite")
    st.header("Fernando de Oliveira Cláudio")
    st.markdown("""
    ---
    **Especialista Certificado:** CEA | ANCORD | CPA-20
    
    Focado em clientes com patrimônio acima de **R$ 300.000,00**, utilizo tecnologia e análise quantitativa 
    para garantir que seu capital supere a inflação e atinja metas de longo prazo com segurança.
    
    **Serviços:**
    - Alocação Estratégica (Asset Allocation)
    - Blindagem Patrimonial
    - Planejamento de Independência Financeira
    ---
    """)
    st.button("Agendar Reunião Estratégica via WhatsApp")

# --- RODAPÉ ---
st.sidebar.markdown("---")
st.sidebar.caption("Elite Financial Experience v2.0")