SELECT saidas, id_orgao, cod_pct, percent_rank, dt_calculo
FROM {schema}.tb_saida
WHERE id_orgao = :orgao_id