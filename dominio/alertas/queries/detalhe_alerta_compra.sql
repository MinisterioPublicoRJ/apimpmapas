SELECT
    contratacao,
    dt_contratacao,
    item,
    var_perc
FROM {schema_alertas_compras}.compras_fora_padrao_capital
WHERE contrato_iditem = :alerta_id
