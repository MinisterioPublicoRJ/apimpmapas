SELECT 
    comp_contratacao,
    comp_id_item,
    comp_item
FROM {schema}.mmps_alertas_comp alrt
LEFT JOIN {schema}.hbase_dispensados D ON D.disp_alrt_key = alrt_key
LEFT JOIN {schema}.hbase_dispensados_todos DT ON DT.disp_alrt_key = regexp_replace(alrt_key, "\.[0-9]*$", '')
WHERE D.disp_alrt_key IS NULL AND DT.disp_alrt_key IS NULL
AND alrt.alrt_orgi_orga_dk = :orgao_id
AND alrt.alrt_sigla = :alrt_type