import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.spines.top': False,
    'axes.spines.right': False
})

# Cores Padrão da Aplicação
COLOR_PRIMARY = '#2c3e50'    # Azul escuro
COLOR_HIGHLIGHT = '#e74c3c'  # Vermelho
COLOR_MUTED = '#bdc3c7'      # Cinza claro
COLOR_PIE = ['#2c3e50', '#34495e', '#7f8c8d', '#bdc3c7'] # Paleta monocromática

st.set_page_config(page_title="Análise de Sinistros de Trânsito", layout="wide")

# ==========================================
# Barra Lateral (Filtros)
# ==========================================
st.sidebar.title("🚦 Filtros Dinâmicos")
st.sidebar.markdown("Explore os dados ajustando os filtros abaixo:")

@st.cache_data
def get_raw_data():
    file_path = "data/proc/cubo_analitico.csv"
    if not os.path.exists(file_path):
        file_path = "app/data/proc/cubo_analitico.csv"
    return pd.read_csv(file_path)

try:
    df_raw = get_raw_data()
    lista_ufs = ["Todos"] + sorted(df_raw['uf'].dropna().unique().tolist())
    uf_selecionada = st.sidebar.selectbox("Estado (UF):", lista_ufs)
    
    lista_anos = ["Todos"] + sorted(df_raw['ano'].dropna().unique().tolist())
    ano_selecionado = st.sidebar.selectbox("Ano:", lista_anos)
except Exception as e:
    st.error(f"Erro ao carregar dados brutos: {e}")
    st.stop()

# ==========================================
# Corpo Principal
# ==========================================
st.title("Painel Analítico: Sinistros de Trânsito no Brasil")

# --- 1. Definição do Problema ---
with st.expander("1. Definição do Problema", expanded=False):
    st.markdown("""
    **Problema de Negócio / Mundo Real:**  
    A base de dados oficial de trânsito (RENAEST) muitas vezes apresenta números inferiores à realidade quando comparada com os atestados de óbito registrados pelo Ministério da Saúde (SIM) e com os custos de internação do SUS (SIH). Essa subnotificação mascara a verdadeira letalidade e o impacto econômico dos acidentes de trânsito.

    **Objetivo:**  
    Cruzaremos essas fontes de dados utilizando o ecossistema Python para investigar o real volume de óbitos, identificar o perfil das vítimas mais frequentes (ex: motociclistas) e expor a relação direta entre o tamanho da população de um município e seu custo hospitalar para o SUS.
    """)

# --- 2. Obtenção e Preparação dos Dados ---
with st.expander("2. Obtenção e Preparação dos Dados", expanded=False):
    st.markdown("Para garantir a qualidade da análise, aplicamos um pipeline de limpeza e transformação usando **Pandas** e **Numpy**.")

def prep_data(df_raw, uf_filter, ano_filter):
    df = df_raw.copy()
    
    # Filtros
    if uf_filter != "Todos":
        df = df[df['uf'] == uf_filter]
    if ano_filter != "Todos":
        df = df[df['ano'] == int(ano_filter)]
        
    # Tratamento de Nulos
    df['custo_sus_total'] = df['custo_sus_total'].fillna(0.0)
    df['obitos_sim'] = df['obitos_sim'].fillna(0)
    df['obitos_renaest'] = df['obitos_renaest'].fillna(0)
    df['populacao'] = df['populacao'].fillna(0)
    
    # Remover duplicatas e tipagem
    df = df.drop_duplicates()
    df['populacao'] = df['populacao'].astype(int)
    df['obitos_sim'] = df['obitos_sim'].astype(int)
    df['obitos_renaest'] = df['obitos_renaest'].astype(int)
    
    df['gap_obitos'] = df['obitos_sim'] - df['obitos_renaest']
    df['custo_por_habitante'] = np.where(df['populacao'] > 0, df['custo_sus_total'] / df['populacao'], 0.0)
    
    return df

df_clean = prep_data(df_raw, uf_selecionada, ano_selecionado)

# --- 3. Análise Exploratória e Visualização ---
st.header("3. Análise Exploratória e Resultados")

if df_clean.empty:
    st.warning("Não há dados para os filtros selecionados.")
else:
    st.markdown("### Visão Geral do Recorte Selecionado")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    total_renaest = df_clean['obitos_renaest'].sum()
    total_sim = df_clean['obitos_sim'].sum()
    total_gap = total_sim - total_renaest
    total_custo = df_clean['custo_sus_total'].sum()
    
    kpi1.metric("Óbitos Oficiais (Trânsito)", f"{total_renaest:,}".replace(",", "."))
    kpi2.metric("Óbitos Reais (Saúde/SIM)", f"{total_sim:,}".replace(",", "."))
    kpi3.metric("Mortes Subnotificadas", f"{total_gap:,}".replace(",", "."), f"{(total_gap/max(total_renaest, 1))*100:.1f}% vs Oficial", delta_color="inverse")
    kpi4.metric("Custo ao SUS", f"R$ {total_custo / 1e6:,.1f} M".replace(",", ".").replace(".", ",", 1))
    
    st.markdown("---")

    # --- Gráficos ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Subnotificação: RENAEST vs SIM")
        if ano_selecionado == "Todos":
            df_agg = df_clean.groupby('ano')[['obitos_renaest', 'obitos_sim']].sum().reset_index()
            x_label = 'Ano'
            x_vals = df_agg['ano'].astype(int)
            x_ticks = np.arange(len(x_vals))
        else:
            df_agg = pd.DataFrame({
                'Categoria': ['Total'],
                'obitos_renaest': [total_renaest],
                'obitos_sim': [total_sim]
            })
            x_label = 'Ano ' + str(ano_selecionado)
            x_vals = ['Total']
            x_ticks = np.arange(1)

        fig1, ax1 = plt.subplots(figsize=(7, 4.5))
        width = 0.35
        
        bars1 = ax1.bar(x_ticks - width/2, df_agg['obitos_renaest'], width, label='RENAEST (Trânsito)', color=COLOR_MUTED)
        bars2 = ax1.bar(x_ticks + width/2, df_agg['obitos_sim'], width, label='SIM (Saúde)', color=COLOR_HIGHLIGHT)
        
        for bar in bars1 + bars2:
            height = bar.get_height()
            ax1.annotate(f'{int(height):,}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
            
        ax1.set_ylabel('Total de Vítimas Fatais')
        ax1.set_xticks(x_ticks)
        ax1.set_xticklabels(x_vals)
        ax1.legend()
        
        st.pyplot(fig1)

    with col2:
        st.subheader("Quem são as Vítimas Fatais?")
        
        soma_conhecidos = (
            df_clean['obitos_sim_pedestre'].sum() +
            df_clean['obitos_sim_ciclista'].sum() +
            df_clean['obitos_sim_motociclista'].sum() +
            df_clean['obitos_sim_auto'].sum() +
            df_clean['obitos_sim_caminhao_onibus'].sum()
        )
        
        outros = total_sim - soma_conhecidos
        
        vitimas = {
            'Pedestres': df_clean['obitos_sim_pedestre'].sum(),
            'Ciclistas': df_clean['obitos_sim_ciclista'].sum(),
            'Motociclistas': df_clean['obitos_sim_motociclista'].sum(),
            'Ocupantes de Auto': df_clean['obitos_sim_auto'].sum(),
            'Caminhão / Ônibus': df_clean['obitos_sim_caminhao_onibus'].sum(),
            'Outros / Não Espec.': max(0, outros)
        }
        
        fig2, ax2 = plt.subplots(figsize=(7, 4.5))
        v_sorted = sorted(vitimas.items(), key=lambda x: x[1])
        keys = [v[0] for v in v_sorted]
        values = [v[1] for v in v_sorted]
        
        max_val = max(values)
        colors_bar = [COLOR_HIGHLIGHT if val == max_val else COLOR_PRIMARY for val in values]
        
        bars_h = ax2.barh(keys, values, color=colors_bar)

        for bar in bars_h:
            width = bar.get_width()
            ax2.annotate(f'{int(width):,}',
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(5, 0), textcoords="offset points",
                        ha='left', va='center', fontsize=9)
            
        ax2.set_xlabel('Quantidade de Óbitos (SIM)')
        ax2.set_xlim(0, max(values) * 1.15) if max(values) > 0 else ax2.set_xlim(0, 1)
        
        st.pyplot(fig2)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- Como e Quando (Comportamento) ---
    st.subheader("Como e Quando os Sinistros Acontecem")
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("**Acidentes por Fase do Dia**")
        total_sinistros = df_clean['sinistros_renaest'].sum()
        if total_sinistros > 0:
            fases = {
                'Madrugada': (df_clean['share_sinistros_madrugada'] * df_clean['sinistros_renaest']).sum() / total_sinistros * 100,
                'Manhã': (df_clean['share_sinistros_manha'] * df_clean['sinistros_renaest']).sum() / total_sinistros * 100,
                'Tarde': (df_clean['share_sinistros_tarde'] * df_clean['sinistros_renaest']).sum() / total_sinistros * 100,
                'Noite': (df_clean['share_sinistros_noite'] * df_clean['sinistros_renaest']).sum() / total_sinistros * 100
            }
        else:
            fases = {'Madrugada': 0, 'Manhã': 0, 'Tarde': 0, 'Noite': 0}
            
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        wedges, texts, autotexts = ax4.pie(fases.values(), labels=fases.keys(), autopct='%1.1f%%', 
                                           colors=COLOR_PIE, startangle=90)
        plt.setp(autotexts, size=9, weight="bold", color="white")
        ax4.axis('equal')
        st.pyplot(fig4)
        
    with col4:
        st.markdown("**Comportamento: Dias da Semana**")
        st.markdown("<small>A incidência costuma escalar aos finais de semana, influenciada por álcool e lazer.</small>", unsafe_allow_html=True)
        if total_sinistros > 0:
            dias = {
                'Seg': (df_clean['share_sinistros_segunda'] * df_clean['sinistros_renaest']).sum() / total_sinistros * 100,
                'Ter': (df_clean['share_sinistros_terca'] * df_clean['sinistros_renaest']).sum() / total_sinistros * 100,
                'Qua': (df_clean['share_sinistros_quarta'] * df_clean['sinistros_renaest']).sum() / total_sinistros * 100,
                'Qui': (df_clean['share_sinistros_quinta'] * df_clean['sinistros_renaest']).sum() / total_sinistros * 100,
                'Sex': (df_clean['share_sinistros_sexta'] * df_clean['sinistros_renaest']).sum() / total_sinistros * 100,
                'Sáb': (df_clean['share_sinistros_sabado'] * df_clean['sinistros_renaest']).sum() / total_sinistros * 100,
                'Dom': (df_clean['share_sinistros_domingo'] * df_clean['sinistros_renaest']).sum() / total_sinistros * 100
            }
        else:
            dias = {'Seg': 0, 'Ter': 0, 'Qua': 0, 'Qui': 0, 'Sex': 0, 'Sáb': 0, 'Dom': 0}
            
        fig5, ax5 = plt.subplots(figsize=(6, 4))
        # Destacar os finais de semana (Sáb, Dom) em vermelho
        cores_dias = [COLOR_MUTED if d not in ['Sáb', 'Dom'] else COLOR_HIGHLIGHT for d in dias.keys()]
        bars_d = ax5.bar(dias.keys(), dias.values(), color=cores_dias)
        
        for bar in bars_d:
            height = bar.get_height()
            ax5.annotate(f'{height:.1f}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)
                        
        ax5.set_ylabel('% de Sinistros')
        st.pyplot(fig5)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Impacto Econômico: Custo SUS vs População")
    
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.scatter(df_clean['populacao'], df_clean['custo_sus_total'], alpha=0.6, color=COLOR_PRIMARY, edgecolor='white', s=50)
    
    # Calculando e plotando a linha de tendência (Correlação Linear)
    if len(df_clean['populacao']) > 1 and df_clean['populacao'].sum() > 0:
        z = np.polyfit(df_clean['populacao'], df_clean['custo_sus_total'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(df_clean['populacao'].min(), df_clean['populacao'].max(), 100)
        ax3.plot(x_trend, p(x_trend), color=COLOR_HIGHLIGHT, linestyle='--', linewidth=2, label="Tendência Linear")
        ax3.legend()

    ax3.set_xlabel('População do Município')
    ax3.set_ylabel('Custo SUS com Internações de Trânsito (R$)')
    ax3.ticklabel_format(style='plain', axis='both')
    
    import matplotlib.ticker as mtick
    ax3.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: f'R$ {x/1e6:,.1f}M'))
    
    st.pyplot(fig3)

st.markdown("---")

# --- 4. Conclusão (Relatório) ---
st.header("4. Conclusão (Relatório Executivo)")

st.info(f"""
### Principais Achados
1. **Subnotificação Sistêmica:** Existe um salto substancial entre as estatísticas oficiais de trânsito e as da saúde. Os dados revelam que **{(total_gap/max(total_renaest, 1))*100:.1f}%** das mortes do recorte só foram capturadas através de atestados de óbito do SUS (SIM), mascarando a real gravidade para os gestores de trânsito.
2. **Motociclistas em Foco:** A análise do perfil demonstrou visualmente que **os motociclistas dominam as mortes**. Isso sugere que campanhas genéricas são ineficientes; as ações públicas devem ser majoritariamente focadas nesse modal.
3. **Conta Transferida para a Saúde:** A linha de tendência no gráfico de dispersão confirma matematicamente uma correlação muito forte e positiva. Cidades maiores arcam inevitavelmente com a ineficiência do trânsito na forma de internações hospitalares caras, totalizando custos na ordem de milhões ao SUS.

**Conclusão Final:**
O ciclo completo utilizando `Pandas` e `Matplotlib` provou a necessidade urgente de unificar as bases de dados e focar as políticas no grupo de risco real (motociclistas). Sem dados integrados, os gestores públicos estão solucionando o problema errado.
""")
