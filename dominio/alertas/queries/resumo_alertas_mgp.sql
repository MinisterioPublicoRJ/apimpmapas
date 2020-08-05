WITH last_session AS (
    SELECT dt_partition
    from {schema}.mmps_alerta_sessao s1
    join (
        SELECT max(alrt_session_finish) as alrt_session_finish
        from {schema}.mmps_alerta_sessao
    ) s2 on s1.alrt_session_finish = s2.alrt_session_finish
)
SELECT
    alrt.alrt_sigla,
    alrt.alrt_descricao,
    alrt.alrt_orgi_orga_dk,
    count(alrt.alrt_sigla) as "count"
FROM {schema}.mmps_alertas alrt
WHERE alrt.dt_partition in
    (select dt_partition FROM last_session)
    AND alrt.alrt_orgi_orga_dk = :orgao_id
GROUP BY
    alrt.alrt_sigla,
    alrt.alrt_descricao,
    alrt.alrt_orgi_orga_dk
