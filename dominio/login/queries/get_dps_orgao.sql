SELECT pip_codigo, group_concat(cast(cisp_codigo as string), ',')
FROM {schema}.tb_pip_cisp
WHERE pip_codigo = :orgao
GROUP BY pip_codigo