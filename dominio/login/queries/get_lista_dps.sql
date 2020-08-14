SELECT pip_codigo, group_concat(cast(cisp_codigo as string), ',')
FROM {schema}.tb_pip_cisp
GROUP BY pip_codigo