SELECT 
    alrt_docu_nr_mp,
    docu_nr_externo,
    alrt_date_referencia,
    alrt_info_adicional
FROM {schema}.mmps_alertas_mgp alrt
JOIN {schema_exadata}.mcpr_documento ON alrt_docu_dk = docu_dk
LEFT JOIN {schema}.hbase_dispensados D ON D.disp_alrt_key = alrt_key
LEFT JOIN {schema}.hbase_dispensados_todos DT ON DT.disp_alrt_key = regexp_replace(alrt_key, "\.[0-9]*$", '')
WHERE D.disp_alrt_key IS NULL AND DT.disp_alrt_key IS NULL
AND alrt.alrt_orgi_orga_dk = :orgao_id
AND alrt.alrt_sigla = :alrt_type