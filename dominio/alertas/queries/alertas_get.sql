SELECT t.*, CASE WHEN disp_alrt_key IS NOT NULL THEN 1 ELSE 0 END AS flag_dispensado
FROM (
    SELECT 
        alrt_docu_dk,
        alrt_docu_nr_mp,
        alrt_date_referencia,
        alrt_orgi_orga_dk,
        alrt_dias_referencia,
        'NOID' as alrt_dk,
        alrt_sigla,
        NULL as alrt_descricao,
        NULL as alrt_classe_hierarquia,
        NULL as alrt_docu_nr_externo,
        alrt_key
    FROM {schema}.mmps_alertas_mgp alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT 
        alrt_docu_dk,
        alrt_docu_nr_mp,
        alrt_date_referencia,
        alrt_orgi_orga_dk,
        alrt_dias_referencia,
        'NOID' as alrt_dk,
        alrt_sigla,
        NULL as alrt_descricao,
        NULL as alrt_classe_hierarquia,
        NULL as alrt_docu_nr_externo,
        alrt_key
    FROM {schema}.mmps_alertas_ppfp alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT 
        alrt_docu_dk,
        alrt_docu_nr_mp,
        alrt_date_referencia,
        alrt_orgi_orga_dk,
        alrt_dias_referencia,
        alrt_itcn_dk as alrt_dk,
        alrt_sigla,
        NULL as alrt_descricao,
        NULL as alrt_classe_hierarquia,
        NULL as alrt_docu_nr_externo,
        alrt_key
    FROM {schema}.mmps_alertas_gate alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT 
        alrt_docu_dk,
        alrt_docu_nr_mp,
        alrt_date_referencia,
        alrt_orgi_orga_dk,
        alrt_dias_referencia,
        'NOID' as alrt_dk,
        alrt_sigla,
        NULL as alrt_descricao,
        NULL as alrt_classe_hierarquia,
        NULL as alrt_docu_nr_externo,
        alrt_key
    FROM {schema}.mmps_alertas_vadf alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT 
        alrt_docu_dk,
        alrt_docu_nr_mp,
        alrt_date_referencia,
        alrt_orgi_orga_dk,
        alrt_dias_referencia,
        'NOID' as alrt_dk,
        alrt_sigla,
        NULL as alrt_descricao,
        NULL as alrt_classe_hierarquia,
        NULL as alrt_docu_nr_externo,
        alrt_key
    FROM {schema}.mmps_alertas_ouvi alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT 
        NULL as alrt_docu_dk,
        NULL as alrt_docu_nr_mp,
        NULL as alrt_date_referencia,
        alrt_orgi_orga_dk,
        NULL as alrt_dias_referencia,
        'NOID' as alrt_dk,
        alrt_sigla,
        isps_indicador as alrt_descricao,
        isps_municipio as alrt_classe_hierarquia,
        NULL as alrt_docu_nr_externo,
        alrt_key
    FROM {schema}.mmps_alertas_isps alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT 
        NULL as alrt_docu_dk,
        NULL as alrt_docu_nr_mp,
        NULL as alrt_date_referencia,
        alrt_orgi_orga_dk,
        abr1_nr_procedimentos as alrt_dias_referencia,
        'NOID' as alrt_dk,
        alrt_sigla,
        NULL as alrt_descricao,
        NULL as alrt_classe_hierarquia,
        NULL as alrt_docu_nr_externo,
        alrt_key
    FROM {schema}.mmps_alertas_abr1 alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT 
        alrt_docu_dk,
        alrt_docu_nr_mp,
        alrt_date_referencia,
        alrt_orgi_orga_dk,
        ro_qt_ros_faltantes as alrt_dias_referencia,
        ro_nr_delegacia as alrt_dk,
        alrt_sigla,
        NULL as alrt_descricao,
        NULL as alrt_classe_hierarquia,
        NULL as alrt_docu_nr_externo,
        alrt_key
    FROM {schema}.mmps_alertas_ro alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
) t
LEFT JOIN {schema}.hbase_dispensados ON disp_alrt_key = alrt_key