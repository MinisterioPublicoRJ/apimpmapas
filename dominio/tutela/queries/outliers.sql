SELECT
cod_orgao,
acervo,
cod_atribuicao,
minimo,
maximo,
media,
primeiro_quartil,
mediana,
terceiro_quartil,
iqr,
lout,
hout,
dt_inclusao
FROM {schema}.tb_distribuicao
WHERE cod_orgao = :orgao_id