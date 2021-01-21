SELECT alrt_docu_dk,
alrt_docu_nr_mp,
alrt_docu_date,
alrt_orgi_orga_dk,
alrt_dias_passados,
alrt_dk,
alrt_sigla,
alrt_descricao,
alrt_classe_hierarquia,
alrt_docu_nr_externo
FROM {schema}.mmps_alertas alrt
LEFT JOIN (
    SELECT * FROM {schema}.alerta_desabilitado WHERE resolvido = false
) desabilitar ON alrt_sigla = sigla AND orgao_id = :orgao_id
where alrt.dt_partition = :dt_partition
    AND alrt.alrt_orgi_orga_dk = :orgao_id
    AND desabilitar.sigla IS NULL
