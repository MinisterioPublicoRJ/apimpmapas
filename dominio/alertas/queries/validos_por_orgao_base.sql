SELECT alrt_docu_dk,
alrt_docu_nr_mp,
alrt_docu_date,
alrt_orgi_orga_dk,
alrt_dias_passados,
alrt_dk,
alrt_sigla
FROM {schema}.mmps_alertas alrt
where alrt.dt_partition = :dt_partition
AND alrt.alrt_orgi_orga_dk = :orgao_id
