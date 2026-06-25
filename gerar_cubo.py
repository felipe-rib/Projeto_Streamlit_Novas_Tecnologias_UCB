import pandas as pd
import numpy as np
import os

def gerar_cubo_analitico():
    print("Iniciando a geração do Cubo Analítico v2...")
    
    base_dir = "data/proc/"

    print("Carregando arquivos Parquet fontes...")
    df_mun    = pd.read_parquet(base_dir + "municipios.parquet")
    df_renaest= pd.read_parquet(base_dir + "mun_ano.parquet")
    df_sim    = pd.read_parquet(base_dir + "sim_mun_ano.parquet")
    df_sih    = pd.read_parquet(base_dir + "sih_mun_ano.parquet")
    df_perfil = pd.read_parquet(base_dir + "mun_perfil.parquet")

    print("Padronizando nomenclatura das colunas...")
    df_renaest = df_renaest.rename(columns={
        'n_acidentes': 'sinistros_renaest',
        'obitos': 'obitos_renaest',
        'feridos_ilesos': 'feridos_renaest',
        'acid_com_obito': 'sinistros_com_obito_renaest'
    })
    
    df_sim = df_sim.rename(columns={
        'obitos_pedestre': 'obitos_sim_pedestre',
        'obitos_ciclista': 'obitos_sim_ciclista',
        'obitos_motociclista': 'obitos_sim_motociclista',
        'obitos_auto': 'obitos_sim_auto',
        'obitos_caminhao_onibus': 'obitos_sim_caminhao_onibus',
        'obitos_via_publica': 'obitos_sim_via_publica',
        'obitos_hospital': 'obitos_sim_hospital',
        'obitos_masc': 'obitos_sim_homens',
        'obitos_fem': 'obitos_sim_mulheres',
        'obitos_jovem': 'obitos_sim_jovens_15_29',
        'obitos_idoso': 'obitos_sim_idosos_60mais',
        'obitos_preto_pardo': 'obitos_sim_pretos_pardos'
    })
    
    df_sih = df_sih.rename(columns={
        'n_aih': 'internacoes_sih',
        'obitos_hosp': 'obitos_hospitalares_sih',
        'custo_total': 'custo_sus_total',
        'dias_perm_total': 'dias_internacao_total',
        'aih_motociclista': 'internacoes_sih_motociclistas',
        'aih_pedestre': 'internacoes_sih_pedestres',
        'aih_ciclista': 'internacoes_sih_ciclistas',
        'aih_auto': 'internacoes_sih_auto',
        'aih_caminhao_onibus': 'internacoes_sih_caminhao_onibus',
        'aih_jovem': 'internacoes_sih_jovens_15_29',
        'aih_idoso': 'internacoes_sih_idosos_60mais'
    })

    print("Cruzando tabelas (Left/Outer Joins)...")
    df_cubo = df_renaest.merge(df_sim, on=['codigo_ibge', 'ano'], how='outer')
    
    df_cubo = df_cubo.merge(df_sih, on=['codigo_ibge', 'ano'], how='outer')
    
    # UF redundante para evitar duplicidade de coluna no próximo join
    if 'uf' in df_cubo.columns:
        df_cubo = df_cubo.drop(columns=['uf'])
        
    # Dados Demográficos (Municípios/IBGE)
    df_cubo = df_cubo.merge(df_mun, on='codigo_ibge', how='left')
    
    # Perfil Temporal Trienal
    df_cubo = df_cubo.merge(df_perfil, on='codigo_ibge', how='left')
    
    print("Calculando métricas avançadas (Features)...")
    
    # Preenchimento de Nulos essenciais para matemática
    cols_to_fill = ['populacao', 'obitos_sim', 'obitos_renaest', 'sinistros_renaest', 'internacoes_sih', 'custo_sus_total']
    for col in cols_to_fill:
        if col in df_cubo.columns:
            df_cubo[col] = df_cubo[col].fillna(0)
            
    # Criando métricas normalizadas por 100 mil habitantes
    df_cubo['mortes_sim_por_100k_hab'] = np.where(df_cubo['populacao'] > 0, (df_cubo['obitos_sim'] / df_cubo['populacao']) * 100000, 0)
    df_cubo['mortes_renaest_por_100k_hab'] = np.where(df_cubo['populacao'] > 0, (df_cubo['obitos_renaest'] / df_cubo['populacao']) * 100000, 0)
    df_cubo['custo_sus_per_capita'] = np.where(df_cubo['populacao'] > 0, (df_cubo['custo_sus_total'] / df_cubo['populacao']), 0)
    
    if 'total' in df_cubo.columns:
        fases = ['madrugada', 'manha', 'tarde', 'noite']
        for fase in fases:
            col_origem = f'fase_{fase}'
            if col_origem in df_cubo.columns:
                df_cubo[f'share_sinistros_{fase}'] = np.where(df_cubo['total'] > 0, df_cubo[col_origem] / df_cubo['total'], 0)
                
        dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
        for dia in dias:
            # Padrão no parquet está 'dia_segunda-feira'
            col_origem = f'dia_{dia}-feira' if dia != 'terca' and dia != 'quarta' and dia != 'quinta' and dia != 'sexta' else f'dia_{dia}-feira'
            if dia == 'segunda': col_origem = 'dia_segunda-feira'
            elif dia == 'terca': col_origem = 'dia_terca-feira'
            elif dia == 'quarta': col_origem = 'dia_quarta-feira'
            elif dia == 'quinta': col_origem = 'dia_quinta-feira'
            elif dia == 'sexta': col_origem = 'dia_sexta-feira'
            elif dia == 'sabado': col_origem = 'dia_sabado'
            elif dia == 'domingo': col_origem = 'dia_domingo'
            
            if col_origem in df_cubo.columns:
                df_cubo[f'share_sinistros_{dia}'] = np.where(df_cubo['total'] > 0, df_cubo[col_origem] / df_cubo['total'], 0)

    # Calculando a subnotificação (Gap SIM vs RENAEST)
    df_cubo['gap_sim_renaest_pct'] = np.where(
        df_cubo['obitos_renaest'] > 0, 
        ((df_cubo['obitos_sim'] - df_cubo['obitos_renaest']) / df_cubo['obitos_renaest']) * 100, 
        0
    )
    df_cubo['flag_sub_registro_renaest'] = df_cubo['gap_sim_renaest_pct'] > 50

    output_file = base_dir + "cubo_analitico.csv"
    print(f"Salvando o cubo plano final em CSV...")
    df_cubo.to_csv(output_file, index=False)
    
    print(f"✅ Concluído com sucesso!")
    print(f"   Dimensões do Cubo: {df_cubo.shape[0]} linhas e {df_cubo.shape[1]} colunas.")
    print(f"   Caminho: {output_file}")

if __name__ == "__main__":
    gerar_cubo_analitico()
