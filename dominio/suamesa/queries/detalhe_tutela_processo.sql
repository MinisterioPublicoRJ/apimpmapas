SELECT 
    orgao_id,
    nm_orgao,
    nr_acoes_ultimos_60_dias,
    variacao_12_meses,
    nr_acoes_ultimos_30_dias
FROM {schema}.tb_detalhe_processo
WHERE orgao_id = :orgao_id