SELECT id_orgao,
nome_regra,
media_orgao,
minimo_orgao,
maximo_orgao,
mediana_orgao,
media_pacote,
maximo_pacote,
mediana_pacote 
FROM {schema}.tb_tempo_tramitacao_integrado
WHERE id_orgao = :orgao_id