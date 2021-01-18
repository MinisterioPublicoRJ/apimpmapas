SELECT 
    alrt_docu_nr_mp,
    docu_nr_externo,
    CASE WHEN alrt_sigla = 'IC1A' THEN alrt_date_referencia ELSE docu_dt_cadastro END,
    alrt_dias_referencia
FROM {schema}.mmps_alertas_stao alrt
JOIN {schema_exadata}.mcpr_documento D ON alrt_docu_dk = docu_dk
WHERE alrt.alrt_orgi_orga_dk = :orgao_id
AND alrt.alrt_sigla = :alrt_type