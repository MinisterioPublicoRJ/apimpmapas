SELECT alrt_docu_dk,
alrt_docu_nr_mp,
alrt_docu_nr_externo,
alrt_docu_etiqueta,
alrt_docu_classe,
alrt_docu_date,
alrt_orgi_orga_dk,
alrt_classe_hierarquia,
alrt_dias_passados,
alrt_dk,
alrt_descricao,
alrt_sigla,
alrt_session,
dt_partition
FROM {schema}.mmps_alertas alrt
where alrt.dt_partition =
    (select MAX(dt_partition) FROM {schema}.mmps_alertas)
AND alrt.alrt_orgi_orga_dk = :orgao_id
