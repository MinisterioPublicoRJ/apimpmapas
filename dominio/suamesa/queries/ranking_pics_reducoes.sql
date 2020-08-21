SELECT orgi_nm_orgao, {nm_campo} 
FROM {schema}.tb_detalhe_documentos_orgao
WHERE tipo_detalhe = :tipo_detalhe
AND intervalo = :intervalo
AND cod_pct IN (
    SELECT cod_pct
    FROM {schema}.atualizacao_pj_pacote
    WHERE id_orgao = :orgao_id)
AND {nm_campo} IS NOT NULL
AND {nm_campo} < 0
ORDER BY {nm_campo} ASC
LIMIT :n