SELECT nm_orgao, {nm_campo} 
FROM {schema}.tb_detalhe_processo
WHERE cod_pct IN (
    SELECT cod_pct
    FROM {schema}.atualizacao_pj_pacote
    WHERE id_orgao = :orgao_id)
AND {nm_campo} IS NOT NULL
ORDER BY {nm_campo} DESC
LIMIT :n