SELECT alrt_sigla, COUNT(1)
FROM (
    SELECT alrt_sigla, alrt_key
    FROM {schema}.mmps_alertas_mgp alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT alrt_sigla, alrt_key
    FROM {schema}.mmps_alertas_ppfp alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT alrt_sigla, alrt_key
    FROM {schema}.mmps_alertas_gate alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT alrt_sigla, alrt_key
    FROM {schema}.mmps_alertas_vadf alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT alrt_sigla, alrt_key
    FROM {schema}.mmps_alertas_ouvi alrt
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
LEFT JOIN {schema}.hbase_dispensados ON disp_alrt_key = alrt_key
WHERE disp_alrt_key IS NULL
GROUP BY alrt_sigla