SELECT 
    orgao_id,
    nm_orgao,
    nr_acoes_12_meses_anterior,
    nr_acoes_12_meses_atual,
    variacao_12_meses,
    nr_acoes_60_dias_anterior,
    nr_acoes_ultimos_60_dias,
    variacao_60_dias,
    nr_acoes_30_dias_anterior,
    nr_acoes_ultimos_30_dias,
    variacao_30_dias
FROM {schema}.tb_detalhe_processo
WHERE orgao_id = :orgao_id