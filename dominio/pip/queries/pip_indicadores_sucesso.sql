SELECT orgao_id, indice, tipo
FROM {schema}.tb_pip_indicadores_sucesso
WHERE orgao_id = :orgao_id
