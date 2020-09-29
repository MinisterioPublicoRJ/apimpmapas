SELECT
    nr_entradas_hoje,
    minimo,
    maximo,
    media,
    primeiro_quartil,
    mediana,
    terceiro_quartil,
    iqr,
    lout,
    hout
FROM {schema}.tb_dist_entradas
WHERE comb_orga_dk = :orgao_id
AND comb_cpf = :nr_cpf