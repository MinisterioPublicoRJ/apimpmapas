SELECT 'COMP', contratacao, id_item, contrato_iditem, item
FROM {schema}.atualizacao_pj_pacote
INNER JOIN {schema_alertas_compras}.compras_fora_padrao_capital ON
    var_perc >= 20
LEFT JOIN (
    SELECT * FROM {schema}.alerta_desabilitado WHERE resolvido = false
) desabilitar ON 'COMP' = sigla AND orgao_id = :id_orgao
WHERE
    UPPER(pacote_atribuicao) LIKE '%%CIDADANIA%%' AND orgao_codamp LIKE '%%CAPITAL%%'
    AND id_orgao = :id_orgao
    AND desabilitar.sigla IS NULL
