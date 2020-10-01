SELECT
    alrt.alrt_sigla,
    alrt.alrt_descricao,
    alrt.alrt_orgi_orga_dk,
    count(alrt.alrt_sigla) as "count"
FROM {schema}.mmps_alertas alrt
WHERE alrt.dt_partition =
    (select MAX(dt_partition) FROM {schema}.mmps_alertas)
    AND alrt.alrt_orgi_orga_dk = :id_orgao
GROUP BY
    alrt.alrt_sigla,
    alrt.alrt_descricao,
    alrt.alrt_orgi_orga_dk
