SELECT 
    alrt_date_referencia,
    docu_dt_cadastro
FROM {schema}.mmps_alertas
JOIN {schema_exadata}.mcpr_documento ON docu_dk = alrt_docu_dk
WHERE alrt_docu_dk = :docu_dk
AND alrt_sigla = 'PA1A'