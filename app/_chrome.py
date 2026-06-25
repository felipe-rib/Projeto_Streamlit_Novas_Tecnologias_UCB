"""Chrome corporativo + helpers visuais.

Centraliza paleta, CSS, KPI cards, hero, exec_footer, template Plotly e
helpers de linguagem. Importado por toda página.
"""
from __future__ import annotations
import sys
from pathlib import Path

import streamlit as st
import plotly.io as pio


# ============================================================
# Paleta — 80% dos pixels em PRIMARY + GRAY_LIGHT
# ============================================================
PRIMARY    = "#1f3a5f"   # azul-marinho institucional
ACCENT     = "#5a7ca8"   # azul médio
ACCENT_HOT = "#c47a4e"   # terracota — UM pop por documento, sempre estratégico
GRAY_DARK  = "#3a3f4a"
GRAY_MED   = "#6c7280"
GRAY_LIGHT = "#9ca3af"   # subido de #cdd2da para melhor contraste em projeção
GRAY_VLIGHT = "#cdd2da"  # ainda mais claro, só para áreas grandes
BORDER     = "#e4e7eb"
BG_SOFT    = "#f5f7fa"
BG_HOT     = "#fdf6f0"   # fundo do bloco CTA "sua cidade"

# usados em comparativos (RENAEST registrado vs. SIM real)
COLOR_REGISTRADO = GRAY_LIGHT
COLOR_REAL       = PRIMARY


# ============================================================
# CSS — esconde chrome do Streamlit + Inter + tabela executiva
# ============================================================
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

#MainMenu                                 { visibility: hidden; }
header [data-testid="stToolbar"]          { visibility: hidden; }
footer                                    { visibility: hidden; }
.stDeployButton                           { display: none; }
[data-testid="stStatusWidget"]            { display: none; }
section[data-testid="stSidebarNav"]       { display: none; }

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    color: #3a3f4a;
}

.main .block-container {
    max-width: 1180px;
    padding-top: 2.4rem;
    padding-bottom: 5rem;
}

h1 { font-size: 30px; font-weight: 600; letter-spacing: -0.01em; margin-bottom: 0.25rem; color: #1a1a1a; }
h2 { font-size: 21px; font-weight: 600; color: #1a1a1a; }
h3 { font-size: 16px; font-weight: 600; color: #1a1a1a; }
.stCaption, [data-testid="stCaptionContainer"] p {
    color: #6c7280 !important;
    font-size: 13px;
    line-height: 1.5;
}

/* Tabelas */
.stDataFrame thead th {
    text-transform: uppercase;
    letter-spacing: 0.03em;
    font-size: 11px;
    background: #f5f7fa;
    border-bottom: 2px solid #d0d5dc;
    font-weight: 600;
}
.stDataFrame tbody tr { height: 44px; }
.stDataFrame tbody tr:hover { background-color: #f9fafb; }
.stDataFrame [data-testid="stElementToolbar"] { display: none; }

/* Sidebar */
.sidebar-brand {
    font-size: 14px; font-weight: 600; color: #1a1a1a;
    letter-spacing: 0.02em; padding: 14px 0 4px 0;
}
.sidebar-section {
    font-size: 10px; font-weight: 600; color: #6c7280;
    text-transform: uppercase; letter-spacing: 0.12em;
    margin: 18px 0 6px 0;
}
section[data-testid="stSidebar"] .stButton button {
    background: transparent; border: none; box-shadow: none;
    text-align: left; padding: 6px 0; width: 100%;
    color: #3a3f4a; font-size: 14px; font-weight: 400;
    justify-content: flex-start;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: #f5f7fa; color: #1f3a5f;
}
section[data-testid="stSidebar"] .stButton button[kind="primary"],
section[data-testid="stSidebar"] .stButton button[data-testid="baseButton-primary"] {
    background: #f5f7fa; color: #1f3a5f; font-weight: 600;
    border-left: 3px solid #1f3a5f; border-radius: 0;
    padding-left: 10px;
}

/* Hero */
.exec-hero {
    background: #f5f7fa;
    border-left: 4px solid #1f3a5f;
    padding: 28px 32px;
    margin: 1.4rem 0 1.8rem 0;
}
.exec-hero p { font-size: 17px; line-height: 1.65; color: #3a3f4a; margin: 0; }

/* Leitura caption */
.leitura {
    border-top: 1px solid #e4e7eb;
    padding-top: 10px;
    margin-top: 6px;
    color: #3a3f4a;
    font-size: 13.5px;
    line-height: 1.55;
}
.leitura b { color: #1a1a1a; }

/* Footer corporativo */
.exec-footer {
    margin-top: 4rem;
    padding-top: 12px;
    border-top: 1px solid #e4e7eb;
    color: #9ca3af;
    font-size: 11px;
    letter-spacing: 0.03em;
}

/* Esconde rótulos vazios de st.selectbox / radio quando label_visibility=collapsed */
[data-testid="stWidgetLabel"]:empty { display: none; }

/* Botão primário grande (CTA "Ver diagnóstico") */
.main .stButton button[kind="primary"] {
    background: #c47a4e;
    border: none;
    color: white;
    font-weight: 600;
    font-size: 15px;
    height: 44px;
    border-radius: 4px;
    letter-spacing: 0.02em;
}
.main .stButton button[kind="primary"]:hover {
    background: #b06b40;
    color: white;
}

/* Espaçamento extra entre blocos */
.block-spacer { height: 36px; }

/* Manchete-link signature */
.exec-sig {
    margin-top: 48px; padding-top: 16px;
    border-top: 1px solid #e4e7eb;
    color: #9ca3af; font-size: 12px; font-style: italic;
    line-height: 1.5;
}
</style>
"""


# ============================================================
# Plotly template
# ============================================================
def _registrar_plotly():
    pio.templates["exec"] = pio.templates["plotly_white"].update(
        layout=dict(
            font=dict(family="Inter, sans-serif", size=13, color=GRAY_DARK),
            title=dict(font=dict(size=15, color=PRIMARY)),
            colorway=[PRIMARY, ACCENT, GRAY_DARK, GRAY_MED, GRAY_LIGHT],
            margin=dict(l=40, r=20, t=20, b=40),
            xaxis=dict(showgrid=False, linecolor="#e0e0e0", color=GRAY_MED),
            yaxis=dict(gridcolor="#f0f0f0", zeroline=False, color=GRAY_MED),
            hoverlabel=dict(bgcolor=PRIMARY, font_color="white",
                             font_family="Inter, sans-serif"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
    )
    pio.templates.default = "exec"

PLOTLY_CONFIG = {"displayModeBar": False}


# ============================================================
# Navegação corporativa — 3 zonas
# ============================================================
SIDEBAR_NAV = [
    ("O PROBLEMA", [
        ("Brasil em 2024",            "sintese"),
        ("Onde mais acontece",        "onde"),
        ("Padrões revelados",         "cruzados"),
    ]),
    ("O QUE FAZER", [
        ("Onde agir e como",          "agir"),
    ]),
    ("SUA CIDADE", [
        ("Diagnóstico",                    "diagnostico"),
        ("Comparar com cidades parecidas", "comparativo"),
    ]),
    ("FUNDAMENTAÇÃO", [
        ("Tipos de cidade",    "perfis"),
        ("Como chegamos aqui", "metodologia"),
    ]),
]


def corporate_sidebar(active_key: str) -> str:
    """Renderiza sidebar customizada. Retorna a chave da página ativa."""
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">RENAEST · Painel executivo</div>',
                    unsafe_allow_html=True)
        st.markdown('<div style="color:#6c7280;font-size:11px;">'
                     'Sinistros de trânsito · Brasil · 2022-2024</div>',
                     unsafe_allow_html=True)
        nova_key = active_key
        for section, items in SIDEBAR_NAV:
            st.markdown(f'<div class="sidebar-section">{section}</div>',
                        unsafe_allow_html=True)
            for label, key in items:
                tipo = "primary" if key == active_key else "secondary"
                if st.button(label, key=f"nav_{key}", type=tipo, use_container_width=True):
                    nova_key = key
        st.markdown('<div style="margin-top:28px;color:#9ca3af;font-size:11px;">'
                     'Fonte: Senatran/RENAEST · DATASUS (SIM e SIH)'
                     '</div>', unsafe_allow_html=True)
    return nova_key


# ============================================================
# setup_page + footer
# ============================================================
def setup_page():
    """Chamado no topo de toda página. Injeta CSS, template Plotly."""
    st.set_page_config(
        page_title="RENAEST — Painel executivo",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(_CSS, unsafe_allow_html=True)
    _registrar_plotly()


def exec_footer():
    st.markdown("""
<div class="exec-footer">
RENAEST — Senatran/Ministério dos Transportes · SIM/SIH — DATASUS · Triênio 2022-2024<br>
Painel preparado para apresentação executiva. Reprodutível a partir dos scripts versionados.
</div>
""", unsafe_allow_html=True)


def signature():
    st.markdown("""
<div class="exec-sig">
Cruzamento de RENAEST (Senatran), SIM e SIH (DATASUS/Ministério da Saúde).
</div>
""", unsafe_allow_html=True)


def spacer():
    st.markdown('<div class="block-spacer"></div>', unsafe_allow_html=True)


# ============================================================
# Mapa coroplético do Brasil
# ============================================================
@st.cache_data(show_spinner=False)
def _br_geojson():
    """GeoJSON dos 27 estados brasileiros (sigla em properties.sigla)."""
    import urllib.request, json
    url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/brazil-states.geojson"
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.load(r)


def mapa_uf(df, valor_col: str, hover_label: str, titulo: str = "",
             colorscale=None):
    """Mapa coroplético dos estados (df precisa ter colunas 'uf' e valor_col)."""
    import plotly.express as px
    geo = _br_geojson()
    if colorscale is None:
        colorscale = [(0, "#eaf0f6"), (0.5, "#5a7ca8"), (1, PRIMARY)]
    fig = px.choropleth(
        df, geojson=geo, locations="uf", featureidkey="properties.sigla",
        color=valor_col, color_continuous_scale=colorscale,
        hover_name="uf",
        hover_data={valor_col: ":,.1f", "uf": False},
        labels={valor_col: hover_label},
    )
    fig.update_geos(
        fitbounds="locations", visible=False,
        bgcolor="rgba(0,0,0,0)",
        showcoastlines=False, showland=False, showlakes=False,
    )
    fig.update_layout(
        height=520,
        margin=dict(l=0, r=0, t=20, b=0),
        coloraxis_colorbar=dict(
            thickness=10, len=0.6,
            title=dict(text=hover_label, font=dict(size=11)),
            tickfont=dict(size=10),
        ),
        title=titulo,
    )
    return fig


# ============================================================
# KPI cards
# ============================================================
def kpi_card(label: str, value: str, delta: str = "", primary: bool = False,
              unit: str = "") -> str:
    cor = PRIMARY if primary else GRAY_DARK
    border_color = PRIMARY if primary else BORDER
    unit_html = (f' <span style="font-size:14px;color:{GRAY_MED};font-weight:400;">{unit}</span>'
                  if unit else '')
    return f"""
<div style="
    padding: 22px 20px;
    background: white;
    border: 1px solid {BORDER};
    border-bottom: 3px solid {border_color};
    min-height: 130px;
    display: flex; flex-direction: column; justify-content: space-between;
">
  <div style="font-size: 11px; font-weight: 600; color: {GRAY_MED};
              text-transform: uppercase; letter-spacing: 0.06em;">
    {label}
  </div>
  <div style="font-size: 30px; font-weight: 600; color: {cor};
              line-height: 1.1; margin-top: 6px;">
    {value}{unit_html}
  </div>
  <div style="font-size: 12.5px; color: {GRAY_MED}; margin-top: 6px;">
    {delta}
  </div>
</div>
"""


def kpi_row(cards: list[str]) -> None:
    cols = st.columns(len(cards), gap="medium")
    for col, html in zip(cols, cards):
        col.markdown(html, unsafe_allow_html=True)


# ============================================================
# Hero da síntese — usar UMA vez por documento
# ============================================================
def hero(html: str) -> None:
    st.markdown(f"""
<div class="exec-hero">
<p>{html}</p>
</div>
""", unsafe_allow_html=True)


def manchete(numero: str, sublinha: str, contexto: str = "", fonte: str = "") -> None:
    """Capa do documento: número-âncora dominante (~90px), sublinha grande,
    contexto pequeno. UMA vez por documento."""
    fonte_html = (f'<div style="font-size:12px;color:{GRAY_MED};margin-top:14px;'
                   f'text-transform:uppercase;letter-spacing:0.08em;">{fonte}</div>'
                   if fonte else "")
    ctx_html = (f'<div style="font-size:16px;color:{GRAY_DARK};margin-top:8px;'
                 f'line-height:1.5;">{contexto}</div>' if contexto else "")
    st.markdown(f"""
<div style="margin: 28px 0 36px 0; padding-bottom: 28px;
            border-bottom: 1px solid {BORDER};">
  <div style="font-size: 84px; font-weight: 700; color: {ACCENT_HOT};
              line-height: 0.95; letter-spacing: -0.03em;">
    {numero}
  </div>
  <div style="font-size: 26px; font-weight: 600; color: {PRIMARY};
              line-height: 1.25; margin-top: 14px; max-width: 720px;">
    {sublinha}
  </div>
  {ctx_html}
  {fonte_html}
</div>
""", unsafe_allow_html=True)


def cta_sua_cidade(municipios_df, default_uf="PR", default_mun="MARINGA") -> None:
    """Bloco terracota: 'sua cidade' selectbox + botão pra ir pra Diagnóstico.
    Único pop de cor 'ativa' do documento."""
    st.markdown(f"""
<div style="background: {BG_HOT}; border-left: 4px solid {ACCENT_HOT};
            padding: 24px 28px; margin: 28px 0;">
  <div style="font-size: 11px; font-weight: 600; color: {ACCENT_HOT};
              text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">
    Sua cidade no mapa
  </div>
  <div style="font-size: 17px; color: {GRAY_DARK}; line-height: 1.5;">
    Selecione abaixo o estado e o município para ver o diagnóstico completo,
    cruzando o registro do trânsito com o registro do Ministério da Saúde
    e os custos do SUS.
  </div>
</div>
""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 3, 2])
    with c1:
        ufs = sorted(municipios_df["uf"].dropna().unique().tolist())
        uf_idx = ufs.index(default_uf) if default_uf in ufs else 0
        uf_sel = st.selectbox("Estado", ufs, index=uf_idx, key="cta_uf",
                                label_visibility="collapsed")
    mun_uf = municipios_df[municipios_df["uf"] == uf_sel].sort_values("populacao", ascending=False)
    muns = mun_uf["municipio"].tolist()
    with c2:
        default = default_mun if default_mun in muns else (muns[0] if muns else "")
        mun_sel = st.selectbox("Município", muns,
                                 index=muns.index(default) if default in muns else 0,
                                 key="cta_mun", label_visibility="collapsed")
    with c3:
        if st.button("Ver diagnóstico  →", type="primary",
                       use_container_width=True, key="cta_botao"):
            st.session_state["uf_sel"] = uf_sel
            st.session_state["mun_sel"] = mun_sel
            st.session_state["page"] = "diagnostico"
            st.rerun()


# ============================================================
# Leitura — caption institucional após gráficos
# ============================================================
def leitura(html: str) -> None:
    st.markdown(f'<div class="leitura"><b>Leitura.</b> {html}</div>',
                 unsafe_allow_html=True)


def como_ler(texto: str) -> None:
    """Caption acima do gráfico explicando o que se vê."""
    st.caption(f"**Como ler.** {texto}")


# ============================================================
# Formatadores
# ============================================================
def fmt_int(v) -> str:
    return f"{int(v):,}".replace(",", ".")

def fmt_pct(v, signed: bool = True) -> str:
    sig = "+" if signed and v >= 0 else ""
    return f"{sig}{v:.0f}%"

def fmt_brl(v) -> str:
    if v >= 1e9:
        return f"R$ {v/1e9:,.1f} bilhões".replace(",", ".")
    if v >= 1e6:
        return f"R$ {v/1e6:,.1f} milhões".replace(",", ".")
    if v >= 1e3:
        return f"R$ {v/1e3:,.0f} mil".replace(",", ".")
    return f"R$ {v:,.2f}".replace(",", ".")


def posicao_humana(rank: int | None, total: int = 3562) -> str:
    """Traduz rank_br (1 = pior) em frase legível para um gestor público."""
    if rank is None or rank <= 0:
        return "—"
    perc = rank / total * 100
    if perc <= 10:   return "entre os 10% piores do país"
    if perc <= 25:   return "entre os 25% piores do país"
    if perc <= 50:   return "acima da mediana nacional"
    if perc <= 75:   return "melhor do que a mediana nacional"
    if perc <= 90:   return "entre os 25% melhores do país"
    return "entre os 10% melhores do país"


def flag_sub_registro(letalidade: float, populacao: int = 0) -> str | None:
    """Retorna mensagem quando a letalidade aparente indica sub-registro de
    sinistros sem vítima fatal."""
    if letalidade > 0.5 and populacao > 30_000:
        return ("Quando mais de 50% dos sinistros registrados terminam em "
                 "óbito, há sinal forte de sub-registro: a cidade provavelmente "
                 "só envia ao RENAEST as ocorrências com vítima fatal. O número "
                 "real de sinistros é maior do que o exibido aqui.")
    return None


# ============================================================
# Linguagem natural — traduz códigos da base para texto
# ============================================================
DIA_HUMANO = {
    "dia_segunda-feira": "Segunda", "dia_terca-feira": "Terça",
    "dia_quarta-feira": "Quarta",   "dia_quinta-feira": "Quinta",
    "dia_sexta-feira":  "Sexta",    "dia_sabado": "Sábado",
    "dia_domingo": "Domingo",
}
FASE_HUMANO = {
    "fase_madrugada": "Madrugada", "fase_manha": "Manhã",
    "fase_tarde": "Tarde",         "fase_noite": "Noite",
}
ROD_HUMANO = {
    "rod_municipal": "Vias municipais", "rod_estadual": "Estaduais",
    "rod_federal": "Federais (BR)",
}
TIPO_HUMANO = {
    "tipo_colisao": "Colisão", "tipo_colisao_lateral": "Colisão lateral",
    "tipo_colisao_traseira": "Colisão traseira",
    "tipo_colisao_frontal": "Colisão frontal",
    "tipo_colisao_transversal": "Colisão transversal",
    "tipo_atropelamento_com_pedestre": "Atropelamento de pedestre",
    "tipo_capotamento": "Capotamento", "tipo_tombamento": "Tombamento",
    "tipo_queda": "Queda", "tipo_engavetamento": "Engavetamento",
    "tipo_outros_acidentes_de_transito": "Outros",
}
