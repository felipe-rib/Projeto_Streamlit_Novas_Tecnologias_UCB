# Cubo analítico — dicionário de campos

**Granularidade:** 1 linha = município × ano  
**Período:** 2022, 2023, 2024  
**Linhas:** 16.741 (5.571 municípios × 3 anos)  
**Fontes integradas:** RENAEST (Senatran), SIM e SIH (DATASUS/Ministério da Saúde)  
**Arquivos:** `cubo_analitico.parquet` (preferido para SQL/DuckDB/Polars) · `cubo_analitico.csv` (universal)

---

## Dimensões (chaves e atributos do município)

| Campo | Tipo | Descrição |
|---|---|---|
| `ano` | int | 2022, 2023 ou 2024 |
| `codigo_ibge` | int | Código IBGE de 7 dígitos do município |
| `municipio` | str | Nome do município (maiúsculas, sem acento) |
| `uf` | str | Sigla da unidade federativa |
| `regiao` | str | Norte, Nordeste, Centro-Oeste, Sudeste, Sul |
| `regiao_metropolitana` | str | Nome da RM, se aplicável; "nao" caso contrário |
| `populacao` | int | População do município (média do triênio) |
| `frota` | int | Frota total de veículos |
| `frota_circulante` | int | Frota efetivamente circulante |
| `cluster_id` | int (0-5) | Identificador do tipo de cidade (agrupamento K-Means) |
| `cluster_nome` | str | Nome humano do tipo de cidade |

---

## Métricas RENAEST (Senatran) — por ano

| Campo | Tipo | Descrição |
|---|---|---|
| `sinistros_renaest` | int | Total de sinistros de trânsito registrados |
| `obitos_renaest` | int | Mortes registradas pelo RENAEST |
| `feridos_renaest` | int | Feridos e ilesos envolvidos |
| `sinistros_com_obito_renaest` | int | Sinistros que tiveram ao menos uma vítima fatal |

> RENAEST conta a ocorrência pelo **local do sinistro** (não pelo município de residência da vítima).

---

## Métricas SIM (Sistema de Informações sobre Mortalidade) — por ano

> Mortes pela **Causa Básica CID-10 V01-V99** (causas externas de transporte), agregadas por **município de residência** da vítima.

| Campo | Tipo | Descrição |
|---|---|---|
| `obitos_sim` | int | Total de mortes por causa de transporte |
| `obitos_sim_pedestre` | int | CID V01-V09 |
| `obitos_sim_ciclista` | int | CID V10-V19 |
| `obitos_sim_motociclista` | int | CID V20-V29 |
| `obitos_sim_auto` | int | CID V40-V59 (ocupantes de auto/caminhonete) |
| `obitos_sim_caminhao_onibus` | int | CID V60-V79 |
| `obitos_sim_via_publica` | int | Mortes ocorridas em via pública (LOCOCOR=4) |
| `obitos_sim_hospital` | int | Mortes em ambiente hospitalar (LOCOCOR=1) |
| `obitos_sim_homens` | int | Vítimas do sexo masculino |
| `obitos_sim_mulheres` | int | Vítimas do sexo feminino |
| `obitos_sim_jovens_15_29` | int | Faixa etária 15–29 anos |
| `obitos_sim_idosos_60mais` | int | Faixa etária 60 anos ou mais |
| `obitos_sim_pretos_pardos` | int | Raça/cor declarada preta ou parda |

---

## Métricas SIH (Sistema de Informações Hospitalares) — por ano

> Internações em hospitais do SUS por causa externa de trânsito (qualquer diagnóstico secundário começando com **V**), agregadas pelo **município de residência do paciente**.

| Campo | Tipo | Descrição |
|---|---|---|
| `internacoes_sih` | int | Total de AIHs aprovadas |
| `obitos_hospitalares_sih` | int | Internações que terminaram em óbito |
| `custo_sus_total` | float | Valor total pago pelo SUS (R$) |
| `custo_sus_uti` | float | Parte do custo total atribuível a UTI |
| `dias_internacao_total` | int | Soma de dias de permanência (todas as AIHs) |
| `dias_uti_total` | int | Soma de dias em UTI |
| `internacoes_sih_motociclistas` | int | AIHs com CID-V20–V29 |
| `internacoes_sih_pedestres` | int | AIHs com CID-V01–V09 |
| `internacoes_sih_ciclistas` | int | AIHs com CID-V10–V19 |
| `internacoes_sih_auto` | int | AIHs com CID-V40–V59 |
| `internacoes_sih_caminhao_onibus` | int | AIHs com CID-V60–V79 |
| `internacoes_sih_jovens_15_29` | int | Faixa etária 15–29 anos |
| `internacoes_sih_idosos_60mais` | int | Faixa etária 60+ |

---

## Métricas derivadas (calculadas)

| Campo | Tipo | Fórmula |
|---|---|---|
| `mortes_sim_por_100k_hab` | float | `obitos_sim / populacao × 100.000` |
| `mortes_renaest_por_100k_hab` | float | `obitos_renaest / populacao × 100.000` |
| `sinistros_por_100k_hab` | float | `sinistros_renaest / populacao × 100.000` |
| `internacoes_por_100k_hab` | float | `internacoes_sih / populacao × 100.000` |
| `letalidade_renaest_pct` | float | `obitos_renaest / sinistros_renaest × 100` (% sinistros com vítima fatal) |
| `letalidade_hospitalar_pct` | float | `obitos_hospitalares_sih / internacoes_sih × 100` (mortalidade na internação) |
| `gap_sim_renaest_pct` | float | `(obitos_sim / obitos_renaest − 1) × 100` (quanto SIM excede RENAEST) |
| `cobertura_renaest_pct` | float | `obitos_renaest / obitos_sim × 100` (% das mortes que o RENAEST capta) |
| `custo_sus_per_capita` | float | `custo_sus_total / populacao` |
| `custo_sus_medio_internacao` | float | `custo_sus_total / internacoes_sih` |
| `dias_medio_internacao` | float | `dias_internacao_total / internacoes_sih` |
| `frota_per_capita` | float | `frota / populacao` |
| `share_obitos_sim_motociclista` | float | `obitos_sim_motociclista / obitos_sim × 100` |
| `share_obitos_sim_pedestre` | float | idem para pedestres |
| `share_obitos_sim_auto` | float | idem para ocupantes de auto |
| `share_obitos_sim_via_publica` | float | `obitos_sim_via_publica / obitos_sim × 100` (proxy de socorro frágil) |
| `share_obitos_sim_jovens` | float | % de mortes na faixa 15–29 |
| `share_obitos_sim_homens` | float | % de mortes do sexo masculino |
| `share_obitos_sim_pretos_pardos` | float | % de mortes em pretos e pardos |
| `share_internacoes_motociclistas` | float | % das AIHs de trânsito que são de motociclistas |
| `share_internacoes_pedestres` | float | idem para pedestres |
| `flag_sub_registro_renaest` | bool | `letalidade_renaest_pct > 50 e populacao > 30.000` → cidade provavelmente só envia ao RENAEST as ocorrências com vítima fatal |

---

## Perfil temporal e dos sinistros (RENAEST agregado no triênio, valor repetido nos 3 anos)

> Estes campos não variam por ano — descrevem o perfil agregado da cidade.

| Campo | Tipo | Descrição |
|---|---|---|
| `share_sinistros_madrugada` / `_manha` / `_tarde` / `_noite` | float | Fração dos sinistros por fase do dia |
| `share_sinistros_segunda` … `share_sinistros_domingo` | float | Fração dos sinistros por dia da semana |
| `share_sinistros_via_municipal` / `_estadual` / `_federal` | float | Fração dos sinistros por tipo de via (dos casos preenchidos) |
| `share_tipo_colisao_simples` / `_lateral` / `_traseira` / `_frontal` / `_transversal` | float | Distribuição por tipo de colisão |
| `share_tipo_atropelamento_pedestre` | float | Fração dos sinistros que são atropelamento de pedestre |
| `share_tipo_capotamento` / `_tombamento` / `_queda` / `_engavetamento` / `_outros` | float | Outras naturezas de sinistro |

---

## Limitações que a LLM precisa conhecer

1. **Cobertura desigual do RENAEST.** Municípios com `letalidade_renaest_pct` acima de 30% provavelmente só registram casos fatais. Use `flag_sub_registro_renaest` para filtrar e prefira `obitos_sim` quando quiser falar de mortalidade real.
2. **Local vs residência.** `obitos_renaest` é local do sinistro; `obitos_sim` é município de residência. `gap_sim_renaest_pct` pode ser negativo em capitais que recebem feridos da região metropolitana.
3. **Campos do perfil temporal são triênio.** Não filtre cruzando por ano — eles são idênticos nos 3 anos.
4. **CID V90-V99** (água/ar) ficou fora — escopo aqui é apenas trânsito terrestre.
5. **Cidades com população < 30.000** podem ter razões instáveis. Use sempre filtro de tamanho ao olhar gap ou letalidade.

---

## Exemplos de perguntas que o cubo responde

```sql
-- Top 10 cidades em mortes SIM por 100 mil habitantes em 2024 (≥100k hab)
SELECT municipio, uf, mortes_sim_por_100k_hab
FROM cubo
WHERE ano = 2024 AND populacao >= 100000
ORDER BY mortes_sim_por_100k_hab DESC LIMIT 10;

-- Custo SUS total no Brasil em 2024
SELECT SUM(custo_sus_total) FROM cubo WHERE ano = 2024;

-- UFs com maior subnotificação RENAEST (excluindo capitais-polo)
SELECT uf,
       SUM(obitos_sim) AS sim,
       SUM(obitos_renaest) AS renaest,
       (SUM(obitos_sim) - SUM(obitos_renaest)) AS adicionais
FROM cubo
WHERE ano BETWEEN 2022 AND 2024
GROUP BY uf
HAVING adicionais > 0
ORDER BY adicionais DESC;

-- % de mortes na via pública por região do Brasil
SELECT regiao, SUM(obitos_sim_via_publica)*100.0/SUM(obitos_sim) AS pct_via
FROM cubo GROUP BY regiao;

-- Cidades parecidas com Maringá (PR) — mesmo cluster e porte similar
SELECT municipio, uf, populacao, mortes_sim_por_100k_hab
FROM cubo
WHERE cluster_id = (SELECT cluster_id FROM cubo WHERE municipio='MARINGA' AND uf='PR' AND ano=2024)
  AND populacao BETWEEN 300000 AND 600000
  AND ano = 2024
ORDER BY populacao DESC;
```
