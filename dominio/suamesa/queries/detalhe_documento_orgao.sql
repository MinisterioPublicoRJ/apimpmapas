SELECT tipo_detalhe,
intervalo,
orgi_nm_orgao,
cod_pct,
vist_orgi_orga_dk,
nr_documentos_distintos_atual,
nr_aberturas_vista_atual,
nr_aproveitamentos_atual,
nr_instaurados_atual,
acervo_inicio,
acervo_fim,
variacao_acervo,
nr_documentos_distintos_anterior,
nr_aberturas_vista_anterior,
nr_aproveitamentos_anterior,
nr_instaurados_anterior,
variacao_documentos_distintos,
variacao_aberturas_vista,
variacao_aproveitamentos,
variacao_instaurados
FROM {schema}.tb_detalhe_documentos_orgao
WHERE tipo_detalhe = :tipo_detalhe
AND vist_orgi_orga_dk = :orgao_id
AND intervalo = :intervalo