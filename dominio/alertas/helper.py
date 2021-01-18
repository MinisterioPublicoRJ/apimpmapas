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
list_columns = {
    'PRCR': [['alrt_docu_nr_mp', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'PRCR1': [['alrt_docu_nr_mp', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'PRCR2': [['alrt_docu_nr_mp', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'PRCR3': [['alrt_docu_nr_mp', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'PRCR4': [['alrt_docu_nr_mp', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'COMP': [['contrato', 'iditem', 'item'], ['contrato', 'iditem', 'item']],
    'ISPS': [
        ['descricao', 'classe_hierarquia'],
        ['nome_indicador', 'municipio']
    ],
    'GATE': [
        ['id_alerta', 'alrt_docu_nr_mp', 'num_externo'],
        ['it_gate', 'numero_mprj', 'numero_externo']
    ],
    # 'MCSI':,
    'MVVD': [['alrt_docu_nr_mp', 'num_externo'], ['numero_mprj', 'numero_externo']],
    # 'RO':,
    'BDPA': [
        ['alrt_docu_nr_mp', 'num_externo', 'data_alerta'],
        ['numero_mprj', 'numero_externo', 'dt_fim_prazo']
    ],
    # 'ABR1':,
    'IC1A': [
        ['alrt_docu_nr_mp', 'num_externo', 'data_alerta'],
        ['numero_mprj', 'numero_externo', 'dt_fim_prazo']
    ],
    'PA1A': [
        ['alrt_docu_nr_mp', 'num_externo', 'data_alerta'],
        ['numero_mprj', 'numero_externo', 'dt_fim_prazo']
    ],
    'PPFP': [
        ['alrt_docu_nr_mp', 'num_externo', 'data_alerta'],
        ['numero_mprj', 'numero_externo', 'dt_cadastro_documento']
    ],
    'PPPV': [
        ['alrt_docu_nr_mp', 'num_externo', 'data_alerta'],
        ['numero_mprj', 'numero_externo', 'dt_cadastro_documento']
    ],
    # 'OFFP': [['num_doc', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'OUVI': [['alrt_docu_nr_mp', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'NF30': [
        ['alrt_docu_nr_mp', 'num_externo', 'data_alerta'],
        ['numero_mprj', 'numero_externo', 'data_autuacao']
    ],
    'VADF': [['alrt_docu_nr_mp', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'DT2I': [['alrt_docu_nr_mp', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'DORD': [['alrt_docu_nr_mp', 'num_externo'], ['numero_mprj', 'numero_externo']],
    'DNTJ': [['alrt_docu_nr_mp', 'num_externo'], ['numero_mprj', 'numero_externo']],
}
