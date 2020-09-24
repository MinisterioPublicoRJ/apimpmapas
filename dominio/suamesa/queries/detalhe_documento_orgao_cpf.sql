SELECT tipo_detalhe,
intervalo,
vist_orgi_orga_dk,
pesf_cpf,
nr_documentos_distintos_atual,
nr_aberturas_vista_atual,
nr_aproveitamentos_atual,
nr_instaurados_atual,
nr_documentos_distintos_anterior,
nr_aberturas_vista_anterior,
nr_aproveitamentos_anterior,
nr_instaurados_anterior,
variacao_documentos_distintos,
variacao_aberturas_vista,
variacao_aproveitamentos,
variacao_instaurados
FROM {schema}.tb_detalhe_documentos_orgao_cpf
WHERE tipo_detalhe = :tipo_detalhe
AND vist_orgi_orga_dk = :orgao_id
AND pesf_cpf = :cpf
AND intervalo = :intervalo
