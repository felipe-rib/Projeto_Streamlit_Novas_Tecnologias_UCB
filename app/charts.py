"""Factories Plotly. Paleta fixa para identidade visual da apresentação."""
from __future__ import annotations
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COLOR_OBITO = "#c0392b"     # vermelho
COLOR_GRAVE = "#e67e22"     # laranja
COLOR_LEVE  = "#f1c40f"     # amarelo
COLOR_INFO  = "#2c3e50"     # azul-escuro
COLOR_BR    = "#7f8c8d"     # cinza
COLOR_UF    = "#3498db"     # azul
COLOR_MUN   = "#c0392b"     # vermelho (destaque)

TEMPLATE = "plotly_white"


def _base(fig, title=None, h=400):
    fig.update_layout(
        template=TEMPLATE, height=h,
        title=dict(text=title or "", font=dict(size=16)),
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def line_tendencia_obitos(br: pd.DataFrame, uf: pd.DataFrame | None = None, mun: pd.DataFrame | None = None,
                           title: str = "Evolução de óbitos") -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=br["ano"], y=br["obitos"], name="Brasil",
                              line=dict(color=COLOR_BR, width=3), mode="lines+markers"))
    if uf is not None:
        fig.add_trace(go.Scatter(x=uf["ano"], y=uf["obitos"], name="UF",
                                  line=dict(color=COLOR_UF, width=3, dash="dash"), mode="lines+markers", yaxis="y2"))
    if mun is not None:
        fig.add_trace(go.Scatter(x=mun["ano"], y=mun["obitos"], name="Município",
                                  line=dict(color=COLOR_MUN, width=3), mode="lines+markers", yaxis="y2"))
    if uf is not None or mun is not None:
        fig.update_layout(yaxis2=dict(overlaying="y", side="right", showgrid=False, title="UF / Município"))
    fig.update_layout(yaxis=dict(title="Brasil"))
    return _base(fig, title)


def bar_ranking_uf(uf_df: pd.DataFrame, metric: str, ylabel: str, highlight: str | None = None) -> go.Figure:
    d = uf_df.sort_values(metric, ascending=True)
    colors = [COLOR_OBITO if u == highlight else COLOR_INFO for u in d["uf"]]
    fig = go.Figure(go.Bar(x=d[metric], y=d["uf"], orientation="h", marker=dict(color=colors),
                            text=d[metric].round(1), textposition="outside"))
    fig.update_layout(xaxis_title=ylabel, yaxis_title="")
    return _base(fig, h=600)


def pie_perfil(labels, values, title) -> go.Figure:
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.45,
                            marker=dict(colors=px.colors.qualitative.Set2)))
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return _base(fig, title, h=350)


def bar_perfil(labels, values, title, color=COLOR_INFO) -> go.Figure:
    fig = go.Figure(go.Bar(x=labels, y=values, marker_color=color,
                            text=[f"{v:.0%}" if v < 1 else f"{int(v)}" for v in values],
                            textposition="outside"))
    return _base(fig, title, h=350)


def line_mensal(df: pd.DataFrame, title: str) -> go.Figure:
    df = df.copy()
    df["data"] = pd.to_datetime(df["ano"].astype(str) + "-" + df["mes"].astype(str).str.zfill(2) + "-01")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["data"], y=df["n_acidentes"], name="Sinistros",
                              line=dict(color=COLOR_INFO), yaxis="y"))
    fig.add_trace(go.Scatter(x=df["data"], y=df["obitos"], name="Óbitos",
                              line=dict(color=COLOR_OBITO, width=3), yaxis="y2"))
    fig.update_layout(yaxis=dict(title="Sinistros"),
                       yaxis2=dict(title="Óbitos", overlaying="y", side="right", showgrid=False))
    return _base(fig, title)


def scatter_taxa_vs_volume(feat: pd.DataFrame, highlight_ibge: int | None = None) -> go.Figure:
    d = feat.copy()
    d["taxa_obitos_100k"] = d["taxa_obitos_100k"].clip(upper=80)  # cap visual
    fig = px.scatter(d, x="populacao", y="taxa_obitos_100k", size="obitos_3a",
                      color="nome_cluster", log_x=True, hover_data=["municipio", "uf"],
                      title="Mapa Brasil: tamanho da cidade × taxa de óbitos",
                      opacity=0.6, height=500)
    if highlight_ibge is not None:
        h = d[d["codigo_ibge"] == highlight_ibge]
        if not h.empty:
            fig.add_trace(go.Scatter(x=h["populacao"], y=h["taxa_obitos_100k"],
                                       mode="markers+text",
                                       marker=dict(size=22, color="black", symbol="x"),
                                       text=h["municipio"], textposition="top center",
                                       name="Sua cidade", showlegend=True))
    fig.update_layout(template=TEMPLATE,
                       legend=dict(orientation="h", yanchor="bottom", y=-0.3))
    return fig
