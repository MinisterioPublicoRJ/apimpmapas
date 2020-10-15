SELECT orgi_nm_orgao, variacao_acervo 
FROM {schema}.tb_detalhe_documentos_orgao
WHERE tipo_detalhe = :tipo_detalhe
AND intervalo = :intervalo
AND cod_pct IN (
    SELECT cod_pct
    FROM {schema}.atualizacao_pj_pacote
    WHERE id_orgao = :orgao_id)
AND variacao_acervo > 0
ORDER BY variacao_acervo DESC
LIMIT :n