SELECT alrt_sigla, comp_contratacao, comp_id_item, comp_contrato_iditem, comp_item, alrt_key, 0 as flag_dispensado
--, CASE WHEN D.disp_alrt_key IS NULL AND DT.disp_alrt_key IS NULL THEN 0 ELSE 1 END AS flag_dispensado
FROM {schema}.mmps_alertas_comp alrt
--LEFT JOIN {schema}.hbase_dispensados D ON D.disp_alrt_key = alrt_key
--LEFT JOIN {schema}.hbase_dispensados_todos DT ON DT.disp_alrt_key = regexp_replace(alrt_key, "\.[0-9]*$", '')
WHERE alrt.alrt_orgi_orga_dk = :id_orgao
