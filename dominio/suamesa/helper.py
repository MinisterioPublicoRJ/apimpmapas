TUTELA_INVESTIGACOES = [
    51219, 51220, 51221, 51222, 51223,  # Procedimentos Administrativos
    392,                                # Inquérito Civil
    395                                 # Procedimento Preparatório
]

TUTELA_PROCESSOS = [
    441, 177,                 # Ação Civil Pública
    175,                      # Ação Civil Coletiva
    176, 127,                 # Ação de Improbidade Administrativa
    18, 126, 159,             # Ação Rescisória
    320,                      # Execução de TAC
    582, 323,                 # Execução Provisória
    319, 51218, 51217, 51205  # Execução Extrajudicial
]

TUTELA_REGRAS_AJUIZAMENTO = (6251, )
TUTELA_REGRAS_TAC = (6655, 6326)
TUTELA_REGRAS_ARQUIV = (
    7912, 6548, 6326, 6681, 6678, 6645, 6682, 6680, 6679,
    6644, 6668, 6666, 6665, 6669, 6667, 6664, 6655, 6662,
    6659, 6658, 6663, 6661, 6660, 6657, 6670, 6676, 6674,
    6673, 6677, 6675, 6672, 6018, 6341, 6338, 6019, 6017,
    6591, 6339, 6553, 7871, 6343, 6340, 6342, 6021, 6334,
    6331, 6022, 6020, 6593, 6332, 7872, 6336, 6333, 6335,
    7745, 6346, 6345, 6015, 6016, 6325, 6327, 6328, 6329,
    6330, 6337, 6344, 6656, 6671, 7869, 7870, 6324, 7834,
    7737, 6350
)
TUTELA_FINALIZACOES = (
    TUTELA_REGRAS_AJUIZAMENTO +
    TUTELA_REGRAS_TAC +
    TUTELA_REGRAS_ARQUIV
)

PIP_INQUERITOS = [494, 3]  # Inquérito Policial, e Policial Militar em ordem
PIP_PICS = [590]  # Procedimento Investigatório Criminal (PIC)

PIP_FINALIZACOES = (6682, 6669, 6018, 6341, 6338, 6019, 6017, 6591, 6339,
                    7871, 6343, 6340, 6342, 7745, 6346, 7915, 6272, 6253,
                    6392, 6377, 6378, 6359, 6362, 6361, 6436, 6524, 7737,
                    7811, 6625, 6718, 7834, 6350)

# Desarquivamentos servem pra anular andamentos de finalização
# Servem tanto para PIP quanto para Tutela 
DESARQUIVAMENTOS = (6075, 1028, 6798, 7245, 6307, 1027, 7803, 6003, 7802,
                    7801, 6004, 6696)