SELECT alrt_sigla, COUNT(1)
FROM (
    SELECT alrt_sigla, alrt_key
    FROM {schema}.mmps_alertas_mgp alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT alrt_sigla, alrt_key
    FROM {schema}.mmps_alertas_stao alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT alrt_sigla, alrt_key
    FROM {schema}.mmps_alertas_gate alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT alrt_sigla, alrt_key
    FROM {schema}.mmps_alertas_vist alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT alrt_sigla, alrt_key
    FROM {schema}.mmps_alertas_movi alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT alrt_sigla, alrt_key
    FROM {schema}.mmps_alertas_isps alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT alrt_sigla, alrt_key
    FROM {schema}.mmps_alertas_abr1 alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT alrt_sigla, alrt_key
    FROM {schema}.mmps_alertas_ro alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT alrt_sigla, alrt_key
    FROM {schema}.mmps_alertas_comp alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
) t
LEFT JOIN {schema}.hbase_dispensados D ON D.disp_alrt_key = alrt_key
LEFT JOIN {schema}.hbase_dispensados_todos DT ON DT.disp_alrt_key = regexp_replace(alrt_key, "\.[0-9]*$", '')
WHERE D.disp_alrt_key IS NULL AND DT.disp_alrt_key IS NULL
GROUP BY alrt_sigla