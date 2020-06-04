SELECT orgi_nm_orgao, {nm_campo} 
FROM {schema}.tb_detalhe_documentos_orgao
WHERE tipo_detalhe = :tipo_detalhe
AND cod_pct IN (
    SELECT cod_pct
    FROM {schema}.atualizacao_pj_pacote
    WHERE id_orgao = :orgao_id)
AND {nm_campo} IS NOT NULL
ORDER BY {nm_campo} DESC
LIMIT :n