SELECT 
    alrt_key,
    alrt_sigla,
    alrt_orgi_orga_dk,
    ro_nr_delegacia,
    ro_qt_ros_faltantes,
    ro_max_proc
FROM {schema}.mmps_alertas_ro alrt
WHERE alrt.alrt_orgi_orga_dk = :orgao_id