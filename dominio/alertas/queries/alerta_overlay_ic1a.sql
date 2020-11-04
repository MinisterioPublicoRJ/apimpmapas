SELECT 
    alrt_docu_date,
    date_sub(alrt_docu_date, 365),
    alrt_docu_etiqueta
FROM {schema}.mmps_alertas
WHERE alrt_docu_dk = :docu_dk
AND dt_partition = :dt_partition
AND alrt_sigla = 'IC1A'
