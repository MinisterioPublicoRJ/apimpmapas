WITH last_session AS (
    SELECT dt_partition
    from {schema}.mmps_alerta_sessao s1
join (
    SELECT max(alrt_session_finish) as alrt_session_finish
    from {schema}.mmps_alerta_sessao
     ) s2 on s1.alrt_session_finish = s2.alrt_session_finish
)
SELECT alrt_docu_dk,
alrt_docu_nr_mp,
alrt_docu_nr_externo,
alrt_docu_etiqueta,
alrt_docu_classe,
alrt_docu_date,
alrt_orgi_orga_dk,
alrt_classe_hierarquia,
alrt_dias_passados,
alrt_descricao,
alrt_sigla,
alrt_session,
dt_partition
FROM {schema}.mmps_alertas alrt
where alrt.dt_partition in
    (select dt_partition FROM last_session)
    AND alrt.alrt_orgi_orga_dk = :orgao_id
    AND alrt.alrt_sigla = :tipo_alerta
