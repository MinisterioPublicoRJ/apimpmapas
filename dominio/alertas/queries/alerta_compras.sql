SELECT 'COMP', contratacao, id_item, contrato_iditem, item 
FROM {schema}.atualizacao_pj_pacote
INNER JOIN {schema_alertas_compras}.compras_fora_padrao_capital ON
    var_perc >= 20
WHERE 
    UPPER(pacote_atribuicao) LIKE '%%CIDADANIA%%' AND orgao_codamp LIKE '%%CAPITAL%%'
    AND id_orgao = :id_orgao
