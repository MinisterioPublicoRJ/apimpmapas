SELECT 
    alrt_docu_nr_mp,
    docu_nr_externo,
    alrt_date_referencia,
    alrt_info_adicional
FROM {schema}.mmps_alertas_mgp alrt
JOIN {schema_exadata}.mcpr_documento D ON alrt_docu_dk = docu_dk
WHERE alrt.alrt_orgi_orga_dk = :orgao_id
AND alrt.alrt_sigla = :alrt_type