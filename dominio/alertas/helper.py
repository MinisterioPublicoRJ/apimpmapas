ordem = [
    'PRCR',
    'PRCR1',
    'PRCR2',
    'PRCR3',
    'PRCR4',
    'COMP',
    'ISPS',
    'GATE',
    'MCSI',
    'MVVD',
    'RO',
    'BDPA',
    'ABR1',
    'IC1A',
    'PA1A',
    'PPFP',
    'PPPV',
    'OFFP',
    'OUVI',
    'NF30',
    'VADF',
    'DT2I',
    'DORD',
    'DNTJ',
]

# Primeira lista = nome das colunas no serializer
# Segunda lista = nome das colunas no arquivo excel gerado
headers = {
    'PRCR': ['numero_mprj', 'numero_externo'],
    'PRCR1': ['numero_mprj', 'numero_externo'],
    'PRCR2': ['numero_mprj', 'numero_externo'],
    'PRCR3': ['numero_mprj', 'numero_externo'],
    'PRCR4': ['numero_mprj', 'numero_externo'],
    'COMP': ['contrato', 'iditem', 'item'],
    'ISPS': ['nome_indicador', 'municipio'],
    'GATE': ['it_gate', 'numero_mprj', 'numero_externo'],
    # 'MCSI':,
    'MVVD': ['numero_mprj', 'numero_externo'],
    # 'RO':,
    'BDPA': ['numero_mprj', 'numero_externo', 'dt_fim_prazo'],
    # 'ABR1':,
    'IC1A': ['numero_mprj', 'numero_externo', 'dt_fim_prazo'],
    'PA1A': ['numero_mprj', 'numero_externo', 'dt_fim_prazo'],
    'PPFP': ['numero_mprj', 'numero_externo', 'dt_cadastro_documento'],
    'PPPV': ['numero_mprj', 'numero_externo', 'dt_cadastro_documento'],
    # 'OFFP': ['numero_mprj', 'numero_externo'],
    'OUVI': ['numero_mprj', 'numero_externo'],
    'NF30': ['numero_mprj', 'numero_externo', 'data_autuacao'],
    'VADF': ['numero_mprj', 'numero_externo'],
    'DT2I': ['numero_mprj', 'numero_externo'],
    'DORD': ['numero_mprj', 'numero_externo'],
    'DNTJ': ['numero_mprj', 'numero_externo'],
}
