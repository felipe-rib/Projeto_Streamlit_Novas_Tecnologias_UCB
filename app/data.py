"""Carregamento + cache dos parquets gerados pelo ETL."""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st

PROC = Path(__file__).resolve().parent.parent / "data" / "proc"

ANOS = (2022, 2023, 2024)
BR_OBITOS_24 = None  # preenchido em load_br


@st.cache_data(show_spinner=False)
def load_municipios() -> pd.DataFrame:
    return pd.read_parquet(PROC / "municipios.parquet")


@st.cache_data(show_spinner=False)
def load_mun_ano() -> pd.DataFrame:
    return pd.read_parquet(PROC / "mun_ano.parquet")


@st.cache_data(show_spinner=False)
def load_mun_mes() -> pd.DataFrame:
    return pd.read_parquet(PROC / "mun_mes.parquet")


@st.cache_data(show_spinner=False)
def load_uf_ano() -> pd.DataFrame:
    return pd.read_parquet(PROC / "uf_ano.parquet")


@st.cache_data(show_spinner=False)
def load_br_ano() -> pd.DataFrame:
    return pd.read_parquet(PROC / "br_ano.parquet")


@st.cache_data(show_spinner=False)
def load_features() -> pd.DataFrame:
    return pd.read_parquet(PROC / "mun_features.parquet")


@st.cache_data(show_spinner=False)
def load_clusters() -> pd.DataFrame:
    return pd.read_parquet(PROC / "mun_clusters.parquet")


@st.cache_data(show_spinner=False)
def load_cluster_perfil() -> pd.DataFrame:
    return pd.read_parquet(PROC / "cluster_perfil.parquet")


@st.cache_data(show_spinner=False)
def load_mun_perfil() -> pd.DataFrame:
    return pd.read_parquet(PROC / "mun_perfil.parquet")


@st.cache_data(show_spinner=False)
def load_mun_vitimas() -> pd.DataFrame:
    return pd.read_parquet(PROC / "mun_vitimas.parquet")


@st.cache_data(show_spinner=False)
def load_mun_modal() -> pd.DataFrame:
    return pd.read_parquet(PROC / "mun_modal.parquet")


@st.cache_data(show_spinner=False)
def load_validacao() -> pd.DataFrame:
    """Cruzamento RENAEST x SIM x SIH. POC com PR+RS no triênio 2022-2024."""
    p = PROC / "mun_validacao.parquet"
    if not p.exists():
        return pd.DataFrame()
    return pd.read_parquet(p)


def has_validacao() -> bool:
    return (PROC / "mun_validacao.parquet").exists()


def kpi_brasil() -> dict:
    br = load_br_ano().sort_values("ano")
    last = br.iloc[-1]
    prev = br.iloc[-2] if len(br) >= 2 else last
    return {
        "obitos_24": int(last["obitos"]),
        "obitos_23": int(prev["obitos"]),
        "obitos_3a": int(br["obitos"].sum()),
        "acid_24": int(last["n_acidentes"]),
        "feridos_3a": int(br["feridos_ilesos"].sum()),
        "delta_obitos_pct": (last["obitos"] / prev["obitos"] - 1) * 100,
        "obitos_dia": last["obitos"] / 365,
    }
