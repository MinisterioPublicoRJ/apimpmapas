SELECT
    dt_contratacao,
    item
FROM {schema_alertas_compras}.compras_fora_padrao_capital
WHERE contrato_iditem = :alerta_id
