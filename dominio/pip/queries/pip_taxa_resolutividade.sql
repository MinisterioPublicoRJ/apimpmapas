SELECT (nr_denuncias_periodo_atual + nr_arquivamentos_periodo_atual + nr_acordos_periodo_atual) / nr_aberturas_vista_periodo_atual
FROM {schema}.tb_pip_detalhe_aproveitamentos
WHERE orgao_id = :orgao_id
