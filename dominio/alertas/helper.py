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
    # 'BDPA',
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
list_columns = {
    'PRCR': [['num_doc', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'PRCR1': [['num_doc', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'PRCR2': [['num_doc', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'PRCR3': [['num_doc', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'PRCR4': [['num_doc', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'COMP': [['contrato', 'iditem', 'item'], ['contrato', 'iditem', 'item']],
    'ISPS': [
        ['descricao', 'classe_hierarquia'],
        ['nome_indicador', 'municipio']
    ],
    'GATE': [
        ['id_alerta', 'num_doc', 'num_externo'],
        ['it_gate', 'numero_mprj', 'numero_externo']
    ],
    # 'MCSI':,
    'MVVD': [['num_doc', 'num_externo'], ['numero_mprj', 'numero_externo']],
    # 'RO':,
    'BDPA': [
        ['num_doc', 'num_externo', 'data_alerta'],
        ['numero_mprj', 'numero_externo', 'dt_fim_prazo']
    ],
    # 'ABR1':,
    'IC1A': [
        ['num_doc', 'num_externo', 'data_alerta'],
        ['numero_mprj', 'numero_externo', 'dt_fim_prazo']
    ],
    'PA1A': [
        ['num_doc', 'num_externo', 'data_alerta'],
        ['numero_mprj', 'numero_externo', 'dt_fim_prazo']
    ],
    'PPFP': [
        ['num_doc', 'num_externo', 'data_alerta'],
        ['numero_mprj', 'numero_externo', 'dt_cadastro_documento']
    ],
    'PPPV': [
        ['num_doc', 'num_externo', 'data_alerta'],
        ['numero_mprj', 'numero_externo', 'dt_cadastro_documento']
    ],
    # 'OFFP': [['num_doc', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'OUVI': [['num_doc', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'NF30': [
        ['num_doc', 'num_externo', 'data_alerta'],
        ['numero_mprj', 'numero_externo', 'data_autuacao']
    ],
    'VADF': [['num_doc', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'DT2I': [['num_doc', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'DORD': [['num_doc', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'DNTJ': [['num_doc', 'num_externo'], ['numero_mprj', 'numero_externo']],
}
