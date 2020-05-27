SELECT
    orgao_id,
    nm_orgao,
    nr_aproveitamentos_periodo_atual,
    nr_aproveitamentos_periodo_anterior,
    variacao_periodo,
    tamanho_periodo_dias
FROM {schema}.tb_pip_detalhe_aproveitamentos