SELECT *
FROM {schema}.tb_detalhe_documentos_orgao_cpf
WHERE tipo_detalhe = :tipo_detalhe
AND vist_orgi_orga_dk = :orgao_id
AND pesf_cpf = :cpf
AND intervalo = :intervalo
