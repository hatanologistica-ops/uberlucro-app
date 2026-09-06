import streamlit as st
import datetime
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="UberLucro Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; padding-bottom: 120px; }
    [data-testid="stHeader"] { display: none; }
    
    .glide-card-verde {
        background-color: #16a34a;
        color: white;
        padding: 22px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    .card-title { font-size: 13px; font-weight: 500; opacity: 0.9; text-transform: uppercase; }
    .card-value { font-size: 34px; font-weight: 800; margin-top: 5px; margin-bottom: 15px; }
    .card-grid { display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 12px; }
    .grid-item { text-align: center; font-size: 13px; }
    .grid-label { opacity: 0.8; font-size: 11px; margin-bottom: 2px; }
    
    .card-mensal-container {
        background-color: #0f172a;
        color: white;
        padding: 20px;
        border-radius: 16px;
        margin-top: 25px;
    }
    .mensal-grid { display: flex; justify-content: space-between; margin-top: 15px; }
    
    .glide-card-branco {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 18px;
        border-radius: 14px;
        margin-bottom: 15px;
    }
    .branco-title { font-size: 12px; color: #64748b; font-weight: 500; }
    .branco-value { font-size: 22px; font-weight: 700; color: #0f172a; margin-top: 4px; }
    
    .nav-bar {
        position: fixed; bottom: 0; left: 0; width: 100%; background-color: #ffffff; 
        border-top: 1px solid #e2e8f0; padding: 12px 0; display: flex; justify-content: space-around; 
        box-shadow: 0px -4px 15px rgba(0,0,0,0.05); z-index: 99999;
    }
    .nav-item { text-align: center; color: #64748b; font-size: 11px; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

st.title("📱 UberLucro Pro")
st.markdown("---")

if 'banco_dados' not in st.session_state:
    st.session_state.banco_dados = []

if 'tela_ativa' not in st.session_state:
    st.session_state.tela_ativa = "Resumo"

col_btn1, col_btn2, col_btn3 = st.columns(3)
if col_btn1.button("📋 Resumo de Hoje", use_container_width=True): st.session_state.tela_ativa = "Resumo"
if col_btn2.button("🚗 Minhas Jornadas", use_container_width=True): st.session_state.tela_ativa = "Jornadas"
if col_btn3.button("📊 Análises de Pista", use_container_width=True): st.session_state.tela_ativa = "Analises"

if st.session_state.tela_ativa == "Resumo":
    st.subheader("Resumo de Hoje")
    
    if len(st.session_state.banco_dados) == 0:
        st.info("Nenhuma jornada registrada hoje. Vá em 'Minhas Jornadas' para fazer o seu primeiro lançamento!")
        lucro_hoje, ganho_hoje, combustivel_hoje, km_rodado_hoje, depreciacao_hoje = 0.0, 0.0, 0.0, 0.0, 0.0
    else:
        ultimo = st.session_state.banco_dados[-1]
        ganho_hoje = ultimo['ganho']
        combustivel_hoje = ultimo['combustivel']
        km_rodado_hoje = ultimo['km_final'] - ultimo['km_inicial']
        depreciacao_hoje = km_rodado_hoje * 0.30
        lucro_hoje = ganho_hoje - combustivel_hoje - depreciacao_hoje - ultimo['outros']

    st.markdown(f"""
        <div class="glide-card-verde">
            <div class="card-title">Lucro Líquido Real</div>
            <div class="card-value">R$ {lucro_hoje:.2f}</div>
            <div class="card-grid">
                <div class="grid-item"><div class="grid-label">Bruto</div><b>R$ {ganho_hoje:.2f}</b></div>
                <div class="grid-item"><div class="grid-label">Combustível</div><b>-R$ {combustivel_hoje:.2f}</b></div>
                <div class="grid-item"><div class="grid-label">Depreciação</div><b>-R$ {depreciacao_hoje:.2f}</b></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.tela_ativa == "Jornadas":
    st.subheader("Registrar uma jornada")
    
    data = st.date_input("Data do Turno", value=datetime.date.today(), format="DD/MM/YYYY")
    ganho_bruto = st.number_input("Ganho Bruto do Dia (R$)", min_value=0.0, value=0.0, step=10.0)
    km_inicial = st.number_input("Quilometragem Inicial (KM Inicial)", min_value=0, value=0)
    km_final = st.number_input("Quilometragem Final (KM Final)", min_value=0, value=0)
    combustivel = st.number_input("Gasto com Combustível (R$)", min_value=0.0, value=0.0, step=5.0)
    outros = st.number_input("Outros Gastos (Almoço/Água) (R$)", min_value=0.0, value=0.0)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("➕ Adicionar lançamento", type="primary", use_container_width=True):
        if ganho_bruto == 0.0 and km_inicial == 0 and km_final == 0:
            st.warning("⚠️ Alerta: Você não preencheu os itens da jornada! Deseja registrar uma jornada zerada mesmo?")
            col_t1, col_t2 = st.columns(2)
            if col_t1.button("Sim, salvar zerado"):
                st.session_state.banco_dados.append({'semana': 'Semana 1', 'ganho': 0.0, 'km_inicial': 0, 'km_final': 0, 'combustivel': 0.0, 'outros': 0.0})
                st.success("Gravado!")
        else:
            if km_final < km_inicial:
                st.error("Erro: O KM Final não pode ser menor que o KM Inicial!")
            else:
                num_sem = f"Semana {(len(st.session_state.banco_dados) // 7) + 1}"
                st.session_state.banco_dados.append({
                    'semana': num_sem, 'ganho': ganho_bruto, 'km_inicial': km_inicial,
                    'km_final': km_final, 'combustivel': combustivel, 'outros': outros
                })
                st.success("Jornada gravada com sucesso!")

    st.markdown("### Histórico recente")
    if len(st.session_state.banco_dados) == 0:
        st.write("Nenhum histórico disponível.")
    else:
        for idx, j in enumerate(reversed(st.session_state.banco_dados)):
            lucro_j = j['ganho'] - j['combustivel'] - ((j['km_final']-j['km_inicial'])*0.30) - j['outros']
            st.markdown(f"""
                <div style="background-color:#f8fafc; border:1px solid #e2e8f0; padding:12px; border-radius:10px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                    <div><b>{j['semana']}</b> — {j['km_final']-j['km_inicial']} km rodados</div>
                    <div style="color:#16a34a; font-weight:bold;">R$ {lucro_j:.2f}</div>
                </div>
            """, unsafe_allow_html=True)

elif st.session_state.tela_ativa == "Analises":
    st.subheader("Análises e Fechamento de Caixa")
    
    if len(st.session_state.banco_dados) == 0:
        st.info("Insira lançamentos na aba 'Minhas Jornadas' para carregar os gráficos e as estimativas mensais.")
    else:
        df_real = pd.DataFrame(st.session_state.banco_dados)
        df_real['km_rodado'] = df_real['km_final'] - df_real['km_inicial']
        df_real['Lucro Líquido'] = df_real['ganho'] - df_real['combustivel'] - (df_real['km_rodado']*0.30) - df_real['outros']
        
        df_semanal = df_real.groupby('semana').agg({'ganho': 'sum', 'Lucro Líquido': 'sum'}).reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_semanal['semana'], y=df_semanal['ganho'], name='Lucro Bruto',
            marker_color='#1e3a8a', text=df_semanal['ganho'], texttemplate='R$ %{text:.2f}', textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            x=df_semanal['semana'], y=df_semanal['Lucro Líquido'], name='Lucro Líquido',
            marker_color='#16a34a', text=df_semanal['Lucro Líquido'], texttemplate='R$ %{text:.2f}', textposition='outside'
        ))
        
        fig.update_traces(marker_line_width=0, cornerradius=10)
        
        fig.update_layout(
            barmode='group', plot_bgcolor='#f8fafc', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#0f172a', title="Resumo Semanal Comparativo",
            yaxis_title="Valores em Reais (R$)", xaxis_title="Semanas de Turno",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        tot_bruto = df_real['ganho'].sum()
        tot_liquido = df_real['Lucro Líquido'].sum()
        tot_despesas = df_real['combustivel'].sum() + (df_real['km_rodado'].sum()*0.30) + df_real['outros'].sum()
        
        st.markdown(f"""
            <div class="card-mensal-container">
                <div style="font-size:14px; font-weight:bold; color:#8bd3dd; text-transform:uppercase;">📊 FECHAMENTO HISTÓRICO MENSAL</div>
                <div style="font-size:36px; font-weight:800; color:#2ecc71; margin-top:5px;">R$ {tot_liquido:.2f}</div>
                <div class="mensal-grid">
                    <div><small style="color:#64748b;">Ganhos Brutos</small><br><b>R$ {tot_bruto:.2f}</b></div>
                    <div><small style="color:#64748b;">Custos Totais</small><br><b style="color:#f43f5e;">-R$ {tot_despesas:.2f}</b></div>
                    <div><small style="color:#64748b;">Semanas Ativas</small><br><b>{df_semanal['semana'].nunique()} sem</b></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
    <div class="nav-bar">
        <div class="nav-item"><div class="nav-icon">📋</div>Resumo</div>
        <div class="nav-item"><div class="nav-icon">🚗</div>Jornadas</div>
        <div class="nav-item"><div class="nav-icon">📊</div>Análises</div>
    </div>
""", unsafe_allow_html=True)
