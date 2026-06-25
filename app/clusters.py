"""Nomes e recomendações por cluster.

IDs vêm do KMeans (random_state=42) em 02_eda_clusters.py. A interpretação
abaixo foi derivada da inspeção dos perfis medianos e dos municípios-âncora
de cada grupo.
"""

CLUSTER_INFO = {
    0: {
        "nome": "Metrópoles costeiras de perfil urbano denso",
        "descricao": (
            "Capitais e municípios de região metropolitana com transporte coletivo "
            "consolidado, vias urbanas e alta densidade. Modal automóvel dominante e "
            "presença relevante de motocicleta."
        ),
        "alerta": "Letalidade moderada-alta; concentração noturna.",
        "acoes": [
            "Fiscalização eletrônica em corredores arteriais",
            "Programa de segurança ao pedestre nas áreas centrais",
            "Reforço noturno (blitz álcool, lei seca) sexta a domingo",
        ],
        "ancoras": ["RIO DE JANEIRO", "RECIFE", "TERESINA", "DUQUE DE CAXIAS"],
    },
    1: {
        "nome": "Cidades médias do interior com alta taxa de óbitos",
        "descricao": (
            "Municípios médios com taxa de óbitos por 100 mil habitantes acima da "
            "média nacional. Frequentemente cidades-polo regionais cortadas por "
            "rodovias estaduais; presença forte de motocicleta como modal."
        ),
        "alerta": "Taxa de óbitos acima da média nacional.",
        "acoes": [
            "Educação para motociclista (capacete, habilitação)",
            "Auditoria de trechos urbanos críticos (cruzamentos)",
            "Integração com Polícia Rodoviária Estadual",
        ],
        "ancoras": ["CAUCAIA", "SOBRAL", "CRATO", "CUBATAO"],
    },
    2: {
        "nome": "Capitais estruturadas com boa cobertura de registro",
        "descricao": (
            "Capitais e cidades grandes em que sinistros leves também chegam ao "
            "RENAEST. Letalidade baixa, volume absoluto elevado, predomínio de "
            "colisões em vias municipais."
        ),
        "alerta": "Volume alto, perfil mais leve.",
        "acoes": [
            "Engenharia viária (semaforização inteligente)",
            "Análise de pontos críticos por mapa de calor",
            "Continuidade no programa de fiscalização",
        ],
        "ancoras": ["BRASILIA", "BELO HORIZONTE", "UBERLANDIA", "JOINVILLE"],
    },
    3: {
        "nome": "Cobertura crítica — apenas óbitos chegam ao sistema",
        "descricao": (
            "Letalidade aparente próxima a 1 óbito por sinistro registrado. Indica "
            "subnotificação de sinistros não-fatais. Inclui Porto Alegre, Manaus, "
            "São Luís e Cuiabá."
        ),
        "alerta": "Sub-registro grave: taxas absolutas dessas cidades estão subestimadas.",
        "acoes": [
            "Prioridade: integrar registros municipais ao RENAEST",
            "Boletim eletrônico de ocorrência com geolocalização",
            "Acordo com Detran e PRF para envio sistemático",
        ],
        "ancoras": ["MANAUS", "PORTO ALEGRE", "SAO LUIS", "CUIABA"],
    },
    4: {
        "nome": "Cidades cortadas por rodovia federal",
        "descricao": (
            "Municípios com ao menos 10% dos sinistros em BR. Padrão típico de "
            "cidades em corredores logísticos; veículos pesados ganham peso."
        ),
        "alerta": "Risco em trechos urbanos de BR; colisões de alta energia.",
        "acoes": [
            "Travessias seguras nas BRs (passarelas, lombadas eletrônicas)",
            "Articulação com DNIT e PRF",
            "Sinalização de aproximação de área urbana",
        ],
        "ancoras": ["FEIRA DE SANTANA", "VITORIA DA CONQUISTA", "JUAZEIRO", "CAMACARI"],
    },
    5: {
        "nome": "Grandes centros com boa cobertura e perfil sólido",
        "descricao": (
            "São Paulo, Fortaleza, Curitiba, Goiânia, Belém. Volume absoluto alto "
            "com taxas de óbito mais controladas. Mix equilibrado de modais."
        ),
        "alerta": "Volume alto exige programas escaláveis.",
        "acoes": [
            "Programa Vida no Trânsito / Vision Zero",
            "Educação contínua em escolas e empresas",
            "Monitoramento em tempo real",
        ],
        "ancoras": ["SAO PAULO", "FORTALEZA", "CURITIBA", "GOIANIA", "BELEM"],
    },
}


def info(cluster_id: int) -> dict:
    return CLUSTER_INFO.get(int(cluster_id), {
        "nome": f"Cluster {cluster_id}",
        "descricao": "Perfil sem rótulo atribuído.",
        "alerta": "",
        "acoes": [],
        "ancoras": [],
    })
