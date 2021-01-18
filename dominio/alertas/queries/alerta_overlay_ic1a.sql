SELECT 
    alrt_date_referencia,
    date_sub(alrt_date_referencia, 365),
    hierarquia
FROM {schema}.mmps_alertas_stao
JOIN {schema_exadata}.mcpr_sub_andamento ON alrt_stao_dk = stao_dk
JOIN {schema_exadata_aux}.mmps_tp_andamento ON stao_tppr_dk = id
WHERE alrt_docu_dk = :docu_dk
AND alrt_sigla = 'IC1A'
